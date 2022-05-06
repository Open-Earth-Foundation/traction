import Vue from 'vue';
import Vuex from 'vuex';

import acme from '@/store/modules/acme.js';
import alice from '@/store/modules/alice.js';
import openclimate from '@/store/modules/openclimate.js';
import bcgov from '@/store/modules/bcgov.js';
import notifications from '@/store/modules/notifications.js';
import sandbox from '@/store/modules/sandbox.js';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { acme, alice, bcgov, notifications, sandbox, openclimate },
  state: {},
  mutations: {},
  actions: {}
});
