<template>
  <div>
    <v-navigation-drawer permanent class="mx-0">
      <v-system-bar color="rgba(42,80,82)" />
      <v-list>
        <v-list-item class="d-none d-sm-flex">
          <v-avatar color="rgba(42,80,82)">
            <v-icon dark>mdi-account-tie</v-icon>
          </v-avatar>
        </v-list-item>

        <v-list-item link>
          <v-list-item-content>
            <v-list-item-title class="text-h6">
              Manager 1
            </v-list-item-title>
            <v-list-item-subtitle>
              manager@cas.com
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list nav>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item v-for="(item, i) in items" :key="i" :class="item.class">
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'AcmeSidebar',
  data: () => ({
    selectedItem: 1,
    // All just for show, doesn't do anything
    items: [
      {
        text: 'Employees',
        icon: 'mdi-card-account-details',
        class: 'd-none d-sm-flex',
      },
      { text: 'Wallets', icon: 'mdi-account-multiple' },
      { text: 'Starred', icon: 'mdi-star', class: 'd-none d-sm-flex' },
      { text: 'Recent', icon: 'mdi-history', class: 'd-none d-sm-flex' },
      { text: 'Offline', icon: 'mdi-check-circle', class: 'd-none d-sm-flex' },
      { text: 'Uploads', icon: 'mdi-upload', class: 'd-none d-sm-flex' },
      { text: 'Backups', icon: 'mdi-cloud-upload', class: 'd-none d-sm-flex' },
    ],
  }),
};
</script>

<style lang="scss" scoped>
.v-item--active {
  color: rgba(0, 160, 144) !important;
}
</style>
