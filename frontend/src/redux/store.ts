import { configureStore } from '@reduxjs/toolkit';
import hcpReducer from './hcpSlice';
import interactionReducer from './interactionSlice';
import chatReducer from './chatSlice';

export const store = configureStore({
  reducer: {
    hcp: hcpReducer,
    interaction: interactionReducer,
    chat: chatReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
