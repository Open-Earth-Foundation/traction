import { lobService } from '@/services';
import { NotificationTypes } from '@/utils/constants';

// The store module to hold the "Openclimate" tenant components
export default {
  namespaced: true,
  state: {
    ofbMessages: [],
    credentials: [],
    credentialOffers: [],
    tenant: {},
    presentationRequests: []
  },
  getters: {
    ofbMessages: state => state.ofbMessages,
    credentials: state => state.credentials,
    credentialOffers: state => state.credentialOffers,
    tenant: state => state.tenant,
    presentationRequests: state => state.presentationRequests
  },
  mutations: {
    SET_OFB_MESSAGES(state, msgs) {
      state.ofbMessages = msgs;
    },
    SET_LOB_CREDENTIALS(state, creds) {
      state.credentials = creds;
    },
    SET_LOB_CREDENTIAL_OFFERS(state, cred_offers) {
      state.credentialOffers = cred_offers;
    },
    SET_TENANT(state, tenant) {
      state.tenant = tenant;
    },
    SET_PRESENTATION_REQUESTS(state, presentationRequests) {
      state.presentationRequests = presentationRequests;
    }
  },
  actions: {
    // Re-get the relevant info for the Openclimate page
    async refreshLob({ dispatch }) {
      await dispatch('sandbox/refreshCurrentSandbox', {}, { root: true });
      await dispatch('getOfbMessages');
      await dispatch('getCredentials');
      await dispatch('getCredentialOffers');
    },
    // Accept an invitation message
    async accept({ dispatch, state, rootState }, msg) {
      try {
        const response = await lobService.acceptInvitation(rootState.sandbox.currentSandbox.id, state.tenant.id, msg.sender.id, msg.msg);
        if (response) {
          dispatch('notifications/addNotification', {
            message: `Accepted ${msg.msg_type} from ${msg.sender ? msg.sender.name : ''}`,
            type: NotificationTypes.SUCCESS
          }, { root: true });
        }
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while accepting the invitation.',
          consoleError: `Error accepting invitation: ${error}`,
        }, { root: true });
      }
      try {
        await lobService.updateOutOfBandMessageAction(rootState.sandbox.currentSandbox.id, state.tenant.id, msg.id, 'Accepted');
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while setting the invitation message to accepted.',
          consoleError: `Error updating message status: ${error}`,
        }, { root: true });
      }
    },
    async reject({ dispatch, state, rootState }, msg) {
      try {
        // we do not do anything here... no problem report, just mark as rejected
        await lobService.updateOutOfBandMessageAction(rootState.sandbox.currentSandbox.id, state.tenant.id, msg.id, 'Rejected');
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while setting the invitation message to rejected.',
          consoleError: `Error updating message status: ${error}`,
        }, { root: true });
      }
    },
    // Query the showcase API for out of band messages for this tenant
    async getOfbMessages({ commit, dispatch, state, rootState }) {
      try {
        const response = await lobService.getOutOfBandMessages(rootState.sandbox.currentSandbox.id, state.tenant.id);
        commit('SET_OFB_MESSAGES', response.data);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while fetching the Out of Band Messages.',
          consoleError: `Error getting messages: ${error}`,
        }, { root: true });
      }
    },
    // Query the showcase API for out of band messages for this tenant
    async getCredentials({ commit, dispatch, state, rootState }) {
      try {
        const response = await lobService.getCredentials(rootState.sandbox.currentSandbox.id, state.tenant.id);
        commit('SET_LOB_CREDENTIALS', response.data);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while fetching Credentials.',
          consoleError: `Error getting credentials: ${error}`,
        }, { root: true });
      }
    },
    async getCredentialOffers({ commit, dispatch, state, rootState }) {
      try {
        const response = await lobService.getCredentialOffers(rootState.sandbox.currentSandbox.id, state.tenant.id);
        commit('SET_LOB_CREDENTIAL_OFFERS', response.data);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while fetching Credential Offers.',
          consoleError: `Error getting credential offers: ${error}`,
        }, { root: true });
      }
    },
    async acceptCredentialOffer({ dispatch, state, rootState }, cred_issue_id) {
      try {
        await lobService.acceptCredentialOffer(rootState.sandbox.currentSandbox.id, state.tenant.id, cred_issue_id);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while accepting Credential Offer.',
          consoleError: `Error getting credential offers: ${error}`,
        }, { root: true });
      }
    },
    async rejectCredentialOffer({ dispatch, state, rootState }, cred_issue_id) {
      try {
        await lobService.rejectCredentialOffer(rootState.sandbox.currentSandbox.id, state.tenant.id, cred_issue_id);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while reject Credential Offer.',
          consoleError: `Error getting credential offers: ${error}`,
        }, { root: true });
      }
    },
    async getPresentationRequests({ commit, dispatch, state, rootState }) {
      try {
        const response = await lobService.getPresentationRequests(rootState.sandbox.currentSandbox.id, state.tenant.id);
        console.log('Presentation req', response);
        commit('SET_PRESENTATION_REQUESTS', response.data);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while getting Presentation Requests.',
          consoleError: `Error getting presentation requests: ${error}`,
        }, { root: true });
      }
    },
    async acceptPresentationRequest({ dispatch, state, rootState }, pres_req_id) {
      try {
        await lobService.acceptPresentationRequest(rootState.sandbox.currentSandbox.id, state.tenant.id, pres_req_id);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while accepting presentation request.',
          consoleError: `Error accepting presentation request: ${error}`,
        }, { root: true });
      }
    },
    async rejectPresentationRequest({ dispatch, state, rootState }, pres_req_id) {
      try {
        await lobService.rejectPresentationRequest(rootState.sandbox.currentSandbox.id, state.tenant.id, pres_req_id);
      }
      catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while rejecting presentation request.',
          consoleError: `Error rejecting presentation request: ${error}`,
        }, { root: true });
      }
    },
    // Receive an invitation
    async acceptExternal({ dispatch, state, rootState }, msg) {
      let invitation = {};
      try {
        invitation = JSON.parse(Buffer.from(msg.split('=')[1], 'base64').toString());
        console.log('Decoded QR', invitation);
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while decoding the invitation.',
          consoleError: `Error decoding invitation: ${error}`,
        }, { root: true });
      }
      let connection_id = '';
      let sender_id = '';
      let sender_name = '';
      try {
        const response = await lobService.receiveInvitationExternal(rootState.sandbox.currentSandbox.id, state.tenant.id, invitation);
        if (response) {
          console.log(response);
          connection_id = response.data.connection_id;
          sender_id =  response.data.sender_id;
          sender_name =  response.data.sender_name;
          dispatch('notifications/addNotification', {
            message: `Accepted external invitation from ${msg.sender ? msg.sender.name : ''}`,
            type: NotificationTypes.SUCCESS
          }, { root: true });
        }
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while accepting the invitation.',
          consoleError: `Error accepting invitation: ${error}`,
        }, { root: true });
      }
      try {
        await lobService.createOutOfBandMessageAction(rootState.sandbox.currentSandbox.id, state.tenant.id, connection_id, sender_id, state.tenant.id, invitation, sender_name, 'Accepted');
      } catch (error) {
        dispatch('notifications/addNotification', {
          message: 'An error occurred while setting the invitation message to accepted.',
          consoleError: `Error updating message status: ${error}`,
        }, { root: true });
      }
    },
  }
};
