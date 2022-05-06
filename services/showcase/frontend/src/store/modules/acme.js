import { lobService, sandboxService } from '@/services';
import { NotificationTypes } from '@/utils/constants';

// The store module to hold the "Acme" tenant components
export default {
  namespaced: true,
  state: {
    applicants: [],
    selectedApplicant: null,
    tenant: {}
  },
  getters: {
    applicants: state => state.applicants
      ? state.applicants.sort((a, b) => a.name.localeCompare(b.name))
      : [],
    selectedApplicant: state => state.selectedApplicant,
    tenant: state => state.tenant
  },
  mutations: {
    SET_APPLICANTS(state, applicants) {
      state.applicants = applicants;
    },
    SET_SELECTED_APPLICANT(state, applicant) {
      state.selectedApplicant = applicant;
    },
    SET_TENANT(state, tenant) {
      state.tenant = tenant;
    }
  },
  actions: {
    // Send an invitation message to the applicant
    async createInvitation({ dispatch, state, rootState }, applicant) {
      try {
        const response = await lobService.createInvitationApplicant(rootState.sandbox.currentSandbox.id, state.tenant.id, applicant.id);
        if (response) {
          dispatch('notifications/addNotification', {
            message: `Invited applicant ${applicant.alias} to ACME`,
            type: NotificationTypes.SUCCESS
          }, { root: true });
        }
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while inviting the applicant.',
          consoleError: `Error inviting applicant: ${error}`,
        }, { root: true });
      }
    },
    // Get the applicants list
    async getApplicants({ dispatch, commit, rootState }) {
      try {
        const response = await sandboxService.getApplicants(rootState.sandbox.currentSandbox.id);
        commit('SET_APPLICANTS', response.data);
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while fetching applicants.',
          consoleError: `Error getting applicant: ${error}`,
        }, { root: true });
      }
    },
    // Send an presentation request to the applicant
    async requestDegree({ dispatch, state, rootState }, applicant) {
      try {
        const response = await lobService.requestDegree(rootState.sandbox.currentSandbox.id, state.tenant.id, applicant.id);
        if (response) {
          dispatch('notifications/addNotification', {
            message: `Presentation request sent to ${applicant.alias} from ACME`,
            type: NotificationTypes.SUCCESS
          }, { root: true });
        }
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while requesting the degree.',
          consoleError: `Error requesting degree: ${error}`,
        }, { root: true });
      }
    },
    // Issue a Scope 1 GHG 
    async issueGHG({ dispatch, rootState, state }, applicant) {
      try {
        const response = lobService.issueGHG(
          rootState.sandbox.currentSandbox.id,
          state.tenant.id,
          applicant.id
        );
        if (response) {
          dispatch('notifications/addNotification', {
            message: `Issued a HGH Credential from ${state.tenant.name} to ${applicant.name}.`,
            type: NotificationTypes.SUCCESS
          }, { root: true });
        }
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: `An error while issuing the Company to ${applicant.name}.`,
          consoleError: `Error issuing Company: ${error}`,
        }, { root: true });
      }
    },

    // Re-get the relevant info for the Acme page
    async refreshLob({ commit, dispatch }) {
      commit('SET_SELECTED_APPLICANT', null);
      await dispatch('sandbox/refreshCurrentSandbox', {}, { root: true });
      await dispatch('getApplicants');
    },
  }
};
