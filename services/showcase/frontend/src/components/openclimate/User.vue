<template>
  <v-card>
    <v-card-title>
      <v-avatar color="indigo">
        <v-icon dark> person </v-icon>
      </v-avatar>
      <p class="ml-3 pt-4">Openclimate</p>
    </v-card-title>
    <v-card-text>
      <p class="text-center">Openclimate Org</p>
      <hr />
      <p class="mt-3 mb-0">
        <strong>ID:</strong> {{ tenant.id }} <br />
        <strong>Created:</strong> {{ tenant.created_at | formatDate }} <br />
        <strong>Wallet ID:</strong> {{ tenant.wallet_id }} <br />
        <strong>Wallet Key:</strong> {{ tenant.wallet_key }} <br />
        <strong>Public DID:</strong> {{ tenant.public_did }}
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'OpenclimateUser',
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapGetters('openclimate', ['tenant']),
  },
};
</script>

<style>
</style>
