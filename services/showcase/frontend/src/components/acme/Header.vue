<template>
  <v-toolbar light flat prominent>
    <template v-slot:img="{ props }">
      <v-img
        v-bind="props"
        gradient="to top right, rgba(42,80,82,.5), rgba(0,160,144,.8)"
      ></v-img>
    </template>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <v-row>
      <v-col cols="12" sm="6">
        <div v-if="tenant.public_did">
          <v-icon color="success">check_circle_outline</v-icon> CAS
          is an Issuer
          <p class="mt-3 mb-0">
            <strong>Wallet ID:</strong> {{ tenant.wallet_id }} <br />
            <strong>Wallet Key:</strong> {{ tenant.wallet_key }} <br />
            <strong>Public DID:</strong> {{ tenant.public_did }}
          </p>
        </div>
        <div v-else>
          <v-icon color="error">error_outline</v-icon> CAS has not
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
      <v-col cols="12" sm="6" class="text-sm-right">
        <v-btn class="mr-4" icon @click="$emit('refresh')">
          <v-icon>refresh</v-icon>
        </v-btn>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">
              <v-icon>group</v-icon> office-admin-001
            </span>
          </template>
          <span>Not really logged in anywhere, just for show</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-spacer></v-spacer>

    <v-btn icon @click="$emit('refresh')">
      <v-icon>mdi-refresh-auto</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-key</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-cube</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-export</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'AcmeHeader',
  computed: {
    ...mapGetters('acme', ['tenant']),
  },
  methods: {
    ...mapActions('sandbox', ['makeIssuer']),
  },
};
</script>
