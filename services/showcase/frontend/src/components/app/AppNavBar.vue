<template>
  <nav class="navigation-main d-print-none px-md-16 px-4">
    <div class="container">
      <ul>
        <li>
          <router-link :to="{ name: 'Home' }">Home</router-link>
        </li>
        <li>
          <router-link :to="{ name: 'Innkeeper' }">Innkeeper</router-link>
        </li>
        <li>
          <router-link :to="{ name: 'BCGov' }">BCGov</router-link>
        </li>
        <!-- <li>
          <router-link :to="{ name: 'Alice' }">Alice</router-link>
        </li> -->
        <li>
          <router-link :to="{ name: 'Acme' }">CAS</router-link>
        </li>
        <li>
          <router-link :to="{ name: 'Openclimate' }">Enterprise Wallet</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavBar',
};
</script>

<style lang="scss" scoped>
.navigation-main {
  box-shadow: 0 6px 8px -4px #b3b1b3;
  display: flex;
  color: var(--v-themeAccent-base);
  background-color: var(--v-themeBgSecond-base);
  width: 100%;
  -webkit-box-shadow: 0 6px 8px -4px #b3b1b3;
  -moz-box-shadow: 0 6px 8px -4px #b3b1b3;

  .container {
    padding: 0;
    ul {
      display: flex;
      flex-direction: row;
      margin: 0;
      color: #ffffff;
      list-style: none;
      margin-left: -1.7rem;

      li {
        a {
          display: flex;
          font-weight: normal;
          min-height: 2rem;
          color: #ffffff;
          padding: 0.75rem 1rem 0.75rem 1rem;
          text-decoration: none;

          &:focus {
            outline: none;
            outline-offset: 0;
          }
          &:hover {
            text-decoration: underline;
          }
        }

        & ~ li {
          border-left: 1px solid #9b9b9b;
          margin: 0;
        }
      }

      .router-link-exact-active {
        background-color: var(--v-themeBgSecond-lighten2);
        border-bottom: 2px solid var(--v-themeAccent-base);
        font-weight: bold;
      }
    }
  }
}
</style>
