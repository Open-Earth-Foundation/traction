<template >
  <div class="students">
    <v-parallax dark src="@/assets/images/canada-1024x250.jpg" class="faber-header">
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="mb-4" color="#FFF">BC Gov</h1>
          <h4 class="subheading">Companies Registry</h4>
        </v-col>
      </v-row>
    </v-parallax>
    <v-container>
      <div v-if="currentSandbox">
        <v-progress-linear v-if="loading" indeterminate color="#173840" />
        <div v-else>
          <Header @refresh="refreshFaber" />
          <Students />
        </div>
      </div>
      <div v-else>
        No sandbox session set, please go to Innkeeper tab to set that up
      </div>
    </v-container>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

import Header from '@/components/bcgov/Header.vue';
import Students from '@/components/bcgov/Students.vue';

export default {
  name: 'BCGov',
  components: {
    Header,
    Students,
  },
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapGetters('sandbox', ['currentSandbox']),
  },
  methods: {
    ...mapActions('bcgov', ['refreshLob']),
    async refreshFaber() {
      this.loading = true;
      await this.refreshLob();
      this.loading = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.students {
  height: 100%;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande',
    'Lucida Sans', Arial, sans-serif !important;
  background-color: rgb(218, 207, 198) !important;
}
.faber-header {
  h1,
  h4 {
    background-color: rgba(218, 207, 198, 0.4);
    padding: 2px;
    padding: 2px;
  }
  h1 {
    font-size: 7em;
  }
  h4 {
    font-size: 2em;
  }
}
</style>
