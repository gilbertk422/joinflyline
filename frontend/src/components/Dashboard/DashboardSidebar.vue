<template>
  <aside class="c-sidebar">
    <router-link
      class="c-sidebar__logo"
      :to="{ name: 'dashboard-ui-overview' }"
    >
      <img src="@/assets/images/dashboard/logo.svg" alt="Logo" />
    </router-link>
    <nav class="c-sidebar__navigation">
      <ul class="c-sidebar__list">
        <li class="c-sidebar__item">
          <router-link
            class="c-sidebar__link"
            :to="{ name: 'dashboard-ui-overview' }"
          >
            <img
              class="c-sidebar__icon"
              src="@/assets/images/dashboard/home.png"
              alt="Home Icon"
            />
            <img
              class="c-sidebar__icon c-sidebar__icon--active"
              src="@/assets/images/dashboard/home-active.png"
              alt="Home Icon"
            />
          </router-link>
        </li>
        <li class="c-sidebar__item">
          <router-link
            class="c-sidebar__link"
            :to="{ name: 'dashboard-ui-travel' }"
          >
            <img
              class="c-sidebar__icon"
              src="@/assets/images/dashboard/travel.png"
              alt="Travel Icon"
            />
            <img
              class="c-sidebar__icon c-sidebar__icon--active"
              src="@/assets/images/dashboard/travel-active.png"
              alt="Travel Icon"
            />
          </router-link>
        </li>
        <li class="c-sidebar__item">
          <router-link
            class="c-sidebar__link"
            :to="{ name: 'dashboard-ui-account' }"
          >
            <img
              class="c-sidebar__icon"
              src="@/assets/images/dashboard/group.svg"
              alt="Group"
            />
            <img
              class="c-sidebar__icon c-sidebar__icon--active"
              src="@/assets/images/dashboard/group-active.svg"
              alt="Group"
            />
          </router-link>
        </li>
      </ul>
      <div class="c-sidebar__logout" @click="logOut($router)">
        <img
          class="c-sidebar__icon"
          src="@/assets/images/dashboard/logout.png"
          alt=""
        />
        <p>Logout</p>
      </div>
    </nav>
  </aside>
</template>

<script>
import Vuex from "vuex";

export default {
  methods: {
    ...Vuex.mapActions("user", ["logOut"])
  }
};
</script>

<style lang="scss">
.c-sidebar {
  width: 4.4375rem;
  height: 100vh;
  position: fixed;
  top: 0;
  background-color: #fff;
  text-align: center;
  z-index: 1;
  .c-sidebar__logo {
    display: block;
    background-color: #00aeef;
    padding: 0.8125rem 0;
    height: 4.0625rem;
    border-right: 1px solid transparentize(#d3d3d3, 0.8);
  }
  .c-sidebar__navigation {
    border-right: 1px solid #d3d3d3;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: calc(100% - 65px);
  }
  .c-sidebar__list {
    list-style: none;
    padding: 0 0.65rem;
    margin: 1.875rem 0 0;
  }
  .c-sidebar__item {
    margin-bottom: 1.875rem;
  }
  .c-sidebar__item:last-child {
    border-bottom: 1px solid #d8d8d8;
    padding-bottom: 1.875rem;
    margin-bottom: 0;
  }
  .c-sidebar__icon--active {
    display: none;
  }
  .c-sidebar__link.exact-active {
    .c-sidebar__icon {
      display: none;
    }
    .c-sidebar__icon--active {
      display: inline-block;
    }
  }
  .c-sidebar__icon {
    width: 1.9rem;
  }
  .c-sidebar__logout {
    color: #979797;
    padding-top: 4px;
    font-size: 0.75rem;
    cursor: pointer;
  }
}
</style>
