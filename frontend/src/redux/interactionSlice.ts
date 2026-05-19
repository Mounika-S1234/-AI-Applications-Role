import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export interface Interaction {
  id: number;
  hcp_id: number;
  interaction_type: 'call' | 'meeting' | 'email' | 'conference' | 'webinar';
  title: string;
  description?: string;
  summary?: string;
  date: string;
  created_at: string;
  updated_at: string;
}

export interface DraftForm {
  hcp_name: string;
  date: string;
  interaction_type: string;
  sentiment: string;
  brochures_shared: boolean | null;
  title: string;
  description: string;
  products_discussed: string;
  action_items: string[];
}

export interface InteractionState {
  interactions: Interaction[];
  selectedInteraction: Interaction | null;
  loading: boolean;
  error: string | null;
  lastSummary?: string;
  actionItems?: string[];
  draftForm: DraftForm;
}

const defaultDraftForm: DraftForm = {
  hcp_name: '',
  date: new Date().toISOString().slice(0, 10),
  interaction_type: 'call',
  sentiment: '',
  brochures_shared: null,
  title: '',
  description: '',
  products_discussed: '',
  action_items: [],
};

const initialState: InteractionState = {
  interactions: [],
  selectedInteraction: null,
  loading: false,
  error: null,
  draftForm: defaultDraftForm,
};

export const fetchInteractions = createAsyncThunk('interaction/fetchAll', async () => {
  const response = await axios.get(`${API_BASE_URL}/interactions/`);
  return response.data;
});

export const fetchHCPInteractions = createAsyncThunk(
  'interaction/fetchHCPInteractions',
  async (hcpId: number) => {
    const response = await axios.get(`${API_BASE_URL}/interactions/hcp/${hcpId}`);
    return response.data;
  }
);

export const createInteraction = createAsyncThunk('interaction/create', async (data: any) => {
  const response = await axios.post(`${API_BASE_URL}/interactions/`, data);
  return response.data;
});

export const updateInteraction = createAsyncThunk(
  'interaction/update',
  async ({ id, data }: any) => {
    const response = await axios.put(`${API_BASE_URL}/interactions/${id}`, data);
    return response.data;
  }
);

export const logInteractionWithAI = createAsyncThunk(
  'interaction/logWithAI',
  async (data: any) => {
    const response = await axios.post(`${API_BASE_URL}/chat/log-interaction`, data);
    return response.data;
  }
);

export const editInteractionWithAI = createAsyncThunk(
  'interaction/editWithAI',
  async ({ id, data }: any) => {
    const response = await axios.post(`${API_BASE_URL}/chat/edit-interaction/${id}`, data);
    return response.data;
  }
);

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    selectInteraction: (state, action) => {
      state.selectedInteraction = action.payload;
    },
    setDraftForm: (state, action) => {
      state.draftForm = {
        ...state.draftForm,
        ...action.payload,
      };
    },
    resetDraftForm: (state) => {
      state.draftForm = defaultDraftForm;
    },
    clearSelection: (state) => {
      state.selectedInteraction = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.interactions = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch interactions';
      })
      .addCase(fetchHCPInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.interactions = action.payload;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.interactions.push(action.payload);
        state.draftForm = defaultDraftForm;
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        const index = state.interactions.findIndex((i) => i.id === action.payload.id);
        if (index !== -1) {
          state.interactions[index] = action.payload;
        }
      })
      .addCase(logInteractionWithAI.fulfilled, (state, action) => {
        state.lastSummary = action.payload.response;
        state.actionItems = action.payload.action_items;
        const formData = action.payload.form_data || {};
        state.draftForm = {
          ...state.draftForm,
          hcp_name: formData.hcp_name || state.draftForm.hcp_name,
          date: formData.interaction_date || state.draftForm.date,
          interaction_type: formData.interaction_type || state.draftForm.interaction_type,
          sentiment: formData.sentiment || state.draftForm.sentiment,
          brochures_shared: formData.brochures_shared ?? state.draftForm.brochures_shared,
          title: formData.title || state.draftForm.title,
          description: formData.description || state.draftForm.description,
          products_discussed: formData.products_discussed || state.draftForm.products_discussed,
          action_items: formData.action_items || state.draftForm.action_items,
        };
        if (action.payload.interaction_id) {
          const interaction = state.interactions.find((i) => i.id === action.payload.interaction_id);
          if (interaction) {
            interaction.summary = action.payload.response;
          }
        }
      })
      .addCase(editInteractionWithAI.fulfilled, (state, action) => {
        state.lastSummary = action.payload.response;
        state.actionItems = action.payload.action_items;
        const formData = action.payload.form_data || {};
        state.draftForm = {
          ...state.draftForm,
          hcp_name: formData.hcp_name || state.draftForm.hcp_name,
          date: formData.interaction_date || state.draftForm.date,
          interaction_type: formData.interaction_type || state.draftForm.interaction_type,
          sentiment: formData.sentiment || state.draftForm.sentiment,
          brochures_shared: formData.brochures_shared ?? state.draftForm.brochures_shared,
          title: formData.title || state.draftForm.title,
          description: formData.description || state.draftForm.description,
          products_discussed: formData.products_discussed || state.draftForm.products_discussed,
          action_items: formData.action_items || state.draftForm.action_items,
        };
      });
  },
});

export const { selectInteraction, clearSelection, setDraftForm, resetDraftForm } = interactionSlice.actions;
export default interactionSlice.reducer;
