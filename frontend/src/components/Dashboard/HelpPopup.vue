<template>
  <div class="modal-content help-modal">
    <div class="modal-header">
      <div class="modal-header__wrapper">
        <h5 class="modal-title">
          Need some help?
        </h5>
        <button
          @click="onButtonClick"
          type="button"
          class="btn"
          data-dismiss="modal"
        >
          Close
        </button>
      </div>
    </div>
    <div class="modal-body">
      <p>
        If you have any questions, click the chat button in the bottom and we'll
        respond as soon as possible, if your question requires immediate
        attention, contact us below.
      </p>
      <div class="modal-body__contact">
        <div class="modal-body__contact__item">
          <span>Phone Number : </span>
          <span>(469) 389-1572</span>
        </div>
        <div class="modal-body__contact__item">
          <span>Email : </span>
          <span>support@joinflyline.com</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["title", "body", "buttonLabel"],
  name: "BookingPopup",
  methods: {
    onButtonClick() {
      this.$emit("button-click");
    }
  }
};
</script>

<style lang="scss" scoped>
.help-modal {
  width: 341px;
  border: none;
  position: absolute;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
  top: 75px;
  border-radius: 0;
}
.modal-header {
  padding: 0.5rem;
  border: none;

  &__wrapper {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #d8d8d8;
    padding: 0.3rem 0.5rem 0;

    h5 {
      color: black;
      font-family: dona-bold;
      font-size: 1.2rem;
    }
    button {
      font-size: 0.7rem;
    }
  }
}
.modal-body {
  padding: 0.5rem 1rem 1rem;
  border: none;

  p {
    color: #939393;
    font-size: 0.8rem;
  }
  &__contact {
    &__item {
      display: flex;
      margin-bottom: 2px;

      & > span:first-child {
        color: black;
        margin-right: 5px;
        font-family: dona-bold;
        font-size: 0.85rem;
      }
      & > span:last-child {
        color: #939393;
        font-size: 0.8rem;
      }
    }
  }
}
</style>
