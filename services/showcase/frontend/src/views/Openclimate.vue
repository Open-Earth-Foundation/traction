<template>
  <div class="openclimate-profile">
    <v-container>
      <v-app-bar shaped>
        <v-icon x-large color="blue">mdi-face-woman-profile</v-icon>
        <h2 class="ml-4">Organization Profile</h2>
        <v-spacer></v-spacer>

        <v-btn icon @click="refreshOpenclimate">
          <v-icon>refresh</v-icon>
        </v-btn>

        <span class="d-none d-sm-flex">
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon>mdi-heart</v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </span>
      </v-app-bar>
      <v-row>
        <v-col cols="12" sm="6">
          <div v-if="tenant.public_did">
            <v-icon color="success">check_circle_outline</v-icon> Business Wallet
            is an Issuer
          </div>
          <div v-else>
            <v-icon color="error">error_outline</v-icon> Business Wallet has not
            met the criteria to be an Issuer yet

            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  large
                  icon
                  v-bind="attrs"
                  v-on="on"
                  @click="makeIssuer(tenant.id)"
                >
                  <v-icon>forward_to_inbox</v-icon>
                </v-btn>
              </template>
              <span>Request Issuer status</span>
            </v-tooltip>
          </div>
        </v-col>
      </v-row>
      <v-row class="mt-4" v-if="currentSandbox">
        <v-col cols="12" sm="4" md="3">
          <User />
        </v-col>
        <v-col cols="12" sm="8" md="6">
          <CredentialOffers class="mb-4" />
          <PresentationRequests class="mb-4" />
          <Credentials />
        </v-col>
        <v-col cols="12" sm="4" md="3">
          <Messages />
        </v-col>
      </v-row>
      <v-row v-else>
        <p class="mt-10">
          No sandbox session set, please go to Innkeeper tab to set that up
        </p>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

import Credentials from '@/components/openclimate/Credentials.vue';
import CredentialOffers from '../components/openclimate/CredentialOffers.vue';
import Messages from '@/components/openclimate/Messages.vue';
import User from '@/components/openclimate/User.vue';
import PresentationRequests from '../components/openclimate/PresentationRequests.vue';

export default {
  name: 'Openclimate',
  components: {
    Credentials,
    Messages,
    User,
    CredentialOffers,
    PresentationRequests,
  },
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapGetters('sandbox', ['currentSandbox']),
    ...mapGetters('openclimate', ['tenant']),
  },
  methods: {
    ...mapActions('openclimate', ['refreshLob']),
    ...mapActions('sandbox', ['makeIssuer']),
    async refreshOpenclimate() {
      this.loading = true;
      await this.refreshLob();
      this.loading = false;
    },
  },
};
</script>

<style lang="scss">
.openclimate-profile {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif !important;
  background-color: #dbdbdb !important;
}
</style>
