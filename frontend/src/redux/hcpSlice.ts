import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export interface HCP {
  id: number;
  name: string;
  specialty?: string;
  organization?: string;
  email?: string;
  phone?: string;
  location?: string;
  created_at: string;
  updated_at: string;
}

export interface HCPState {
  hcps: HCP[];
  selectedHCP: HCP | null;
  loading: boolean;
  error: string | null;
}

const initialState: HCPState = {
  hcps: [],
  selectedHCP: null,
  loading: false,
  error: null,
};

export const fetchHCPs = createAsyncThunk('hcp/fetchHCPs', async () => {
  const response = await axios.get(`${API_BASE_URL}/hcps/`);
  return response.data;
});

export const createHCP = createAsyncThunk('hcp/createHCP', async (hcpData: any) => {
  const response = await axios.post(`${API_BASE_URL}/hcps/`, hcpData);
  return response.data;
});

export const updateHCP = createAsyncThunk('hcp/updateHCP', async ({ id, data }: any) => {
  const response = await axios.put(`${API_BASE_URL}/hcps/${id}`, data);
  return response.data;
});

export const deleteHCP = createAsyncThunk('hcp/deleteHCP', async (id: number) => {
  await axios.delete(`${API_BASE_URL}/hcps/${id}`);
  return id;
});

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    selectHCP: (state, action) => {
      state.selectedHCP = action.payload;
    },
    clearSelection: (state) => {
      state.selectedHCP = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchHCPs.fulfilled, (state, action) => {
        state.loading = false;
        state.hcps = action.payload;
      })
      .addCase(fetchHCPs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch HCPs';
      })
      .addCase(createHCP.fulfilled, (state, action) => {
        state.hcps.push(action.payload);
      })
      .addCase(updateHCP.fulfilled, (state, action) => {
        const index = state.hcps.findIndex((h) => h.id === action.payload.id);
        if (index !== -1) {
          state.hcps[index] = action.payload;
        }
        if (state.selectedHCP?.id === action.payload.id) {
          state.selectedHCP = action.payload;
        }
      })
      .addCase(deleteHCP.fulfilled, (state, action) => {
        state.hcps = state.hcps.filter((h) => h.id !== action.payload);
        if (state.selectedHCP?.id === action.payload) {
          state.selectedHCP = null;
        }
      });
  },
});

export const { selectHCP, clearSelection } = hcpSlice.actions;
export default hcpSlice.reducer;
