<template>
  <header class="o-main-header">
    <h2 class="o-main-header__title">Travel Portal</h2>
    <form class="o-main-header__form">
      <div class="o-main-header__control">
        <div class="o-main-header__control-inner">
          <label class="control__label" for="round-trip">
            <input
              type="radio"
              name="direction"
              id="round-trip"
              v-model="form.destinationTypeId"
              value="round"
            />
            <span class="o-main-header__control-text">Round-trip</span>
            <div class="control__indicator"></div>
          </label>
        </div>
      </div>
      <div class="o-main-header__control">
        <div class="o-main-header__control-inner">
          <label class="control__label" for="one-way">
            <input
              type="radio"
              name="direction"
              id="one-way"
              v-model="form.destinationTypeId"
              value="oneway"
            />
            <span class="o-main-header__control-text">One-way</span>
            <div class="control__indicator"></div>
          </label>
        </div>
      </div>
      <div class="o-main-header__control">
        <location-input
          input-class="o-main-header__input"
          type="text"
          prompt="Departure City or Airport"
          prompt-mobile="Departure City or Airport"
          prompt-mobile-focus="Departure City or Airport"
          :initial-value="form.placeFrom"
          @place-selected="updatePlaceFrom"
        />
      </div>
      <div class="o-main-header__control">
        <location-input
          input-class="o-main-header__input"
          type="text"
          prompt="Arrival City or Airport"
          prompt-mobile-focus="Arrival City or Airport"
          prompt-mobile="Arrival City or Airport"
          :initial-value="form.placeTo"
          @place-selected="updatePlaceTo"
        />
      </div>
      <div class="o-main-header__control">
        <input
          class="o-main-header__input"
          type="text"
          placeholder="Trip Dates"
          id="flight-dates"
        />
      </div>
      <div class="o-main-header__control">
        <select
          class="o-main-header__input o-main-header__input--select"
          name="level-of-flight"
          id="level-of-flight"
        >
          <option
            v-for="(seatTypeLabel, seatTypeCode) in seatTypes"
            :value="seatTypeCode"
            :key="seatTypeCode"
            >{{ seatTypeLabel }}</option
          >
        </select>
      </div>
      <div class="o-main-header__control">
        <select
          class="o-main-header__input o-main-header__input--select"
          name="number-of-people"
          id="number-of-people"
        >
          <option value="1 Adult">1 Adult</option>
        </select>
      </div>
      <div class="o-main-header__control">
        <a
          type="button"
          @click.prevent="doSearch"
          class="o-main-header__submit"
        >
          <img src="@/assets/images/dashboard/search.png" alt="Search Icon" />
        </a>
      </div>
    </form>
    <div class="o-main-header__questions">
      <div class="o-main-header__questions-inner" @click="handleDlg">
        <img
          class="o-main-header__questions-img"
          src="@/assets/images/dashboard/question.png"
          alt="Question Icon"
        />
      </div>
      <HelpPopup v-if="preFlag" @button-click="handleDlg" />
    </div>
    <div class="o-main-header__profile">
      <div class="o-main-header__profile__wrapper">
        <h4 class="o-main-header__profile-title">
          {{ user.first_name }} {{ user.last_name }}
        </h4>
        <p class="o-main-header__profile-subtitle">Basic : $49.99/yr</p>
      </div>
    </div>
  </header>
</template>

<script>
import LocationInput from "../LocationInput";
import SearchForm from "../SearchForm";
import HelpPopup from "./HelpPopup";
import Vuex from "vuex";

export default {
  extends: SearchForm,
  data() {
    return {
      preFlag: false
    };
  },
  components: {
    LocationInput,
    HelpPopup
  },
  methods: {
    doSearch() {
      this.search({ clearFilters: true, saveSearch: true });
      this.$router.push({ name: "new-results" });
    },
    handleDlg() {
      this.preFlag = !this.preFlag;
    }
  },
  computed: {
    ...Vuex.mapState("user", ["user"])
  }
};
</script>

<style lang="scss">
.o-main-header {
  padding-left: 5.4375rem;
  background-color: #00aeef;
  height: 4.0625rem;
  display: flex;
  position: sticky;
  top: 0;
  z-index: 1;
  .o-main-header__control {
    height: 44px;
    display: flex;
    align-items: center;
    &:nth-child(n + 1) {
      width: 12%;
    }
    &:nth-child(n + 2) {
      width: 12%;
    }
    &:nth-child(n + 3) {
      width: 20%;
      & > div {
        width: 100%;
        & > div {
          width: 100%;
          & > input {
            width: 100%;
          }
        }
      }
    }
    &:nth-child(n + 4) {
      width: 20%;
      & > div {
        width: 100%;
        & > div {
          width: 100%;
          & > input {
            width: 100%;
          }
        }
      }
    }
    &:nth-child(n + 5) {
      width: 15%;
      & > input {
        width: 100%;
      }
    }
    &:nth-child(n + 6) {
      width: 8%;
      & > select {
        width: 100%;
      }
    }
    &:nth-child(n + 7) {
      width: 8%;
      & > select {
        width: 100%;
      }
    }
    &:nth-child(n + 8) {
      width: 5%;
      max-width: 50px;
      & > a {
        width: 100%;
      }
    }
  }
  .o-main-header__title {
    font-family: Dona-Black;
    font-size: 1.25rem;
    margin-bottom: 0;
    color: #fff;
    display: flex;
    align-items: center;
    height: 100%;
    padding-right: 1.0625rem;
    border-right: 1px solid transparentize(#d3d3d3, 0.8);
    width: 10%;
    text-align: center;
  }
  .o-main-header__form {
    display: flex;
    height: 100%;
    align-items: center;
    padding: 0 0.75rem;
    border: 1px solid rgba(211, 211, 211, 0.2);
    width: 75%;
    font-size: 12.8px;
  }
  .o-main-header__input {
    border: 0;
    padding: 0.5rem;
    background-color: rgba(255, 255, 255, 0.4);
    border: 1px solid transparent;
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    color: #fff;
    height: 44px;
    &::placeholder {
      color: transparentize(#fff, 0.5);
    }
    &:focus {
      outline: none;
      border: 1px solid white;
    }
  }
  .o-main-header__input--select {
    border-radius: 0;
    appearance: none;
    option {
      color: black;
    }
  }
  .o-main-header__submit {
    display: inline-flex;
    height: 100%;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.4);
    img {
      width: 70%;
      padding: 0 0.3rem;
    }
  }
  .o-main-header__questions {
    height: 100%;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    border-right: 1px solid transparentize(#d3d3d3, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 5%;
  }
  .o-main-header__questions-inner {
    width: 44px;
    height: 44px;
    background-color: rgba(255, 255, 255, 0.4);
    border-radius: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .o-main-header__questions-img {
    width: 1rem;
  }
  .o-main-header__profile {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-left: 0.8rem;
    width: 10%;
  }
  .o-main-header__profile-title {
    font-family: Dona-Bold;
    margin-bottom: 0.3rem;
    color: #fff;
    font-size: 1.125rem;
  }
  .o-main-header__profile-subtitle {
    color: #fff;
    font-family: Dona-Bold;
    margin-bottom: 0;
    font-size: 0.8rem;
  }
  .control__indicator {
    position: absolute;
    top: 0;
    left: 0;
    height: 20px;
    width: 20px;
    background-color: transparentize(#fff, 0.5);
    border: 0;
    &:after {
      background-color: #fff;
      width: 100%;
      height: 100%;
      content: "";
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      transform: scale(0);
      transition: transform 0.2s ease-in-out;
    }
  }
  .o-main-header__control-inner {
    display: flex;
    align-items: center;
    position: relative;
    padding-left: 30px;
    cursor: pointer;
    font-size: 13px;
    &:first-child {
      margin-right: 18px;
    }
    input {
      position: absolute;
      z-index: -1;
      opacity: 0;
    }
    input:checked ~ .control__indicator:after {
      transform: scale(0.55);
    }
  }
  .o-main-header__control-text {
    font-family: Dona-Bold;
    color: #fff;
  }
  .control__label {
    margin-bottom: 0;
    cursor: pointer;
  }
}

@media (max-width: 1652px) {
  .o-main-header {
    .o-main-header__title {
      font-size: 1.2rem;
      padding: 0 10px 0 0;
    }
  }
}

@media (max-width: 1500px) {
  .o-main-header {
    .o-main-header__title {
      font-size: 1rem;
    }
    .o-main-header__control-text {
      font-size: 0.8rem;
    }
    .o-main-header__control-inner:first-child {
      margin-right: 8px;
    }
  }
}

@media (max-width: 1450px) {
  .o-main-header {
    .o-main-header__profile-title {
      font-size: 0.9rem;
    }
    .o-main-header__profile-subtitle {
      font-size: 0.7rem;
    }
  }
}

@media (max-width: 1310px) {
  .o-main-header {
    .o-main-header__title {
      width: 11%;
      padding: 0 5px 0 0;
    }
    .o-main-header__control-text {
      font-size: 0.7rem;
    }
    .o-main-header__control-inner:first-child {
      margin-right: 8px;
    }
    .o-main-header__form {
      padding: 0.5rem;
    }
    .o-main-header__profile-title {
      font-size: 0.8rem;
    }
  }
}
</style>
