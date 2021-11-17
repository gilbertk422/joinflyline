<template>
  <div class="dashboard">
    <dashboard-header :single-date-field="true" />
    <dashboard-sidebar />
    <main class="o-main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import DashboardSidebar from "./components/Dashboard/DashboardSidebar";
import DashboardHeader from "./components/Dashboard/DashboardHeader";
export default {
  name: "Dashboard",
  components: {
    DashboardSidebar,
    DashboardHeader
  }
};
</script>

<style>
.dashboard {
  height: 100vh;
  background: #f7f9fc;
}
.o-main-content {
  margin-left: 4.4375rem;
  padding: 0 1.0625rem;
  background: #f7f9fc;
}
</style>
