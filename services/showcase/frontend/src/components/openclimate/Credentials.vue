<template>
  <v-card>
    <v-card-title> My Credentials</v-card-title>
    <v-card-text v-if="credentials && credentials.length">
      <v-card v-for="c in credentials" :key="c.id" class="ma-3">
        <v-system-bar v-if="revokedMsg" color="rgba(200, 060, 74)" style="justify-content: center">
          <b style="color: white;font-size: large;">{{ revokedMsg }}</b>
        </v-system-bar>
        <v-card-text>
          <ul>
            <li><b>Schema: </b>{{ c.schema_id }}</li>
            <hr class="my-2" />
            <li>
              <b>Issuer: </b>
              <a target="_blank" :href="nym_link(c.cred_def_id)">
                {{ issuer_name() }}
              </a>
            </li>
            <li>
              <b> Connection to Issuer: </b>
              Active
            </li>
          </ul>
          <v-expansion-panels class="mt-2">
            <v-expansion-panel>
              <v-expansion-panel-header> Details </v-expansion-panel-header>
              <v-expansion-panel-content>
                <div><b>cred_def_id:</b> {{ c.cred_def_id }}</div>
                <div><b>schema_id:</b> {{ c.schema_id }}</div>
                <!-- <div><b>date_received:</b> {{ c.attrs.date }}</div> -->
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
      </v-card>
    </v-card-text>
    <v-card-text v-else> There are no credentials to show </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'OpenclimateCredentials',
  data() {
    return {
      loading: false,
      revokedMsg: undefined
    };
  },
  computed: {
    ...mapGetters('sandbox', ['currentSandbox']),
    ...mapGetters('openclimate', ['credentials', 'ofbMessages']),
  },
  methods: {
    ...mapActions('openclimate', ['getCredentials', 'getOfbMessages']),
    issuer_name() {
      return 'OpenClimate Platform';
    },
    nym_link(cred_def_id) {
      return `http://test.bcovrin.vonx.io/browse/domain?page=1&query=${
        cred_def_id.split(':')[0]
      }&txn_type=1`;
    },
  },
  async mounted() {
    await this.getCredentials();
    await this.getOfbMessages();
    const revoked = this.ofbMessages.find(x => x.msg_type === 'Revocation');
    this.revokedMsg = revoked ? revoked.msg.comment : undefined;
    this.loading = false;
  },
};
</script>

<style>
</style>
