<template>
  <div :class="`toast-item ${typee}`">
    <span>{{ message }}</span>
  </div>
</template>

<script>
export default {
  props: {
    typee: {
      type: String,
      required: false,
      default: "success"
    },
    message: {
      type: String,
      required: false,
      default: "success"
    }
  }
};
</script>

<style lang="scss" scoped>
.toast-item {
  margin-top: 10px;
  padding: 10px 22px 3px;
  font-family: dona-bold;
  font-size: 12px;
  margin-bottom: 10px;

  &.primary {
    background: #daf0fb;
    color: #00aeef;
  }
  &.success {
    background: #c6edda;
    color: #00bd52;
  }
}
</style>
