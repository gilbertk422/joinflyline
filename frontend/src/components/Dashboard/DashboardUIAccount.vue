<template>
  <div class="account-view">
    <modal v-if="subscriptionCancelled">
      <template #body>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Subscription
            </h5>
          </div>
          <div class="modal-body">
            <p>
              You have successfully canceled your free trial. If you end up
              changing your mind, please let us know and we will get you set up!
            </p>
          </div>
          <div class="modal-footer">
            <button
              @click="goToOverview"
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </template>
    </modal>
    <div class="dashboard-section-heading">
      <div class="section-heading__inner">
        <span class="section-heading__title">Travel Portal / </span>
        <span class="section-heading__title section-heading__title__current"
          >Dashboard</span
        >
      </div>
    </div>

    <div class="row account-view-container">
      <div class="account-box travel-information col-6">
        <h4 class="box-header">Traveler Information</h4>
        <hr />
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="First Name"
            v-model="user.first_name"
          />
          <input
            class="row-form-input"
            placeholder="Last Name"
            v-model="user.last_name"
          />
        </div>
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="Date of Birth"
            v-model="dobText"
          />
          <multiselect
            v-model="user.gender"
            :options="genderOptions"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="false"
            label="label"
            track-by="label"
          >
          </multiselect>
        </div>
        <div class="row-form">
          <location-input
            :initial-value="user.market"
            input-class="row-form-input"
            prompt="Home Airport"
            @place-selected="updateHomeAirport"
          />
          <div>
            <input
              class="row-form-input full-width-input"
              placeholder="Phone Number"
              v-model="user.phone_number"
            />
          </div>
        </div>
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="Passport Number"
            v-model="user.passport_number"
          />
          <input
            placeholder="Known Traveler Number"
            class="row-form-input"
            v-model="user.tsa_precheck_number"
          />
        </div>
        <button type="button" @click="saveAccount">Save Information</button>
      </div>
      <div class="account-box freq-question col-6" v-if="frequentflyerReady">
        <h4 class="box-header">Frequent Flyer Miles</h4>
        <hr />
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="American Airlines"
            v-model="frequentflyer.AA"
          />
          <input
            class="row-form-input"
            placeholder="Sun Country Airlines"
            v-model="frequentflyer.SY"
          />
        </div>
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="Delta Airlines"
            v-model="frequentflyer.DL"
          />
          <input
            class="row-form-input"
            placeholder="jetBlue"
            v-model="frequentflyer.B6"
          />
        </div>
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="United Airlines"
            v-model="frequentflyer.UA"
          />
          <input
            class="row-form-input"
            placeholder="Spirit"
            v-model="frequentflyer.NK"
          />
        </div>
        <div class="row-form">
          <input
            class="row-form-input"
            placeholder="Southwest Airlines"
            v-model="frequentflyer.WN"
          />
          <input
            class="row-form-input"
            placeholder="Hawaiian Airlines"
            v-model="frequentflyer.HA"
          />
        </div>
        <button type="button" @click="saveFrequentFlyer">
          Save Information
        </button>
      </div>
      <div class="account-box deal-alert-notification col-6">
        <account-deals />
      </div>
      <div class="account-box additional-users col-6">
        <account-companion v-if="user.role === userRoles.subscriber" />
      </div>
      <div class="account-box-container col-6">
        <h3 class="account__deals__title">Subscription Managment</h3>
        <hr />
        <div class="subscription-management row">
          <div
            class="col-12 col-lg-6 subscription-wrapper"
            v-for="(plan, code) in plans"
            :key="`plan-${code}`"
          >
            <div class="subscription">
              <div class="subscription__top">
                <div class="subscription__title">
                  <h4 class="subscription__heading subscription__heading--type">
                    {{ plan.name }}
                  </h4>
                  <h3
                    v-if="plan.price"
                    class="subscription__heading subscription__heading--price"
                  >
                    ${{ plan.price.value }}/yr
                  </h3>
                  <h3
                    v-else
                    class="subscription__heading subscription__heading--price"
                  >
                    Free
                  </h3>
                </div>
                <ul class="subscription__list">
                  <li class="subscription__item">
                    - Flight Search and Book
                  </li>
                  <li class="subscription__item">- Auto Check-in</li>
                  <li v-if="plan.limit" class="subscription__item">
                    - Max of {{ plan.limit }} Bookings
                  </li>
                  <li v-else class="subscription__item">
                    - Unlimited Bookings
                  </li>
                  <li class="subscription__item">
                    - Access to FlyLine Portal
                  </li>
                  <li v-if="plan.deal_alerts" class="subscription__item">
                    - Deal alerts
                  </li>
                  <li v-if="plan.companion" class="subscription__item">
                    <!-- - {{ plans[pk].companion }} companion account{{ plans[pk].companion>1?"s":"" }} -->
                    - Companion account
                  </li>
                </ul>
              </div>
              <div class="subscription__bottom">
                <button
                  v-if="planStatus(code) === 'current'"
                  class="button button--outline-blue"
                  :disabled="cancelPlanProgress"
                  @click="cancelPlan"
                >
                  Cancel Plan
                </button>
                <button
                  v-else-if="planStatus(code) === 'upgrade'"
                  class="button button--outline-blue"
                >
                  Upgrade plan
                </button>
                <button v-else class="button button--outline-blue">
                  Downgrade plan
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LocationInput from "../LocationInput";
import { airlineIcon, formatDateFull, userRoles } from "../../utils/utils";
import Lightpick from "lightpick";
import api from "../../utils/http";
import moment from "moment";
import Vuex from "vuex";
import { airlineCodes } from "../../utils/airlineCodes";
import { genderOptions } from "../../utils/utils";
import AccountDeals from "../AccountDeals";
import AccountCompanion from "../AccountCompanion";
import { Multiselect } from "vue-multiselect";

const frequentFlyerNames = {
  american_airlines: "AA",
  united_airlines: "UA",
  southwest_airlines: "WN",
  sun_country_airlines: "SY",
  frontier_airlines: "F9",
  delta_airlines: "DL",
  alaska_airlines: "AS",
  jetBlue: "B6",
  spirit_airlines: "NK",
  allegiant_air: "G4",
  hawaiian_airlines: "HA"
};

export default {
  name: "DashboardUIAccount",
  components: { LocationInput, AccountDeals, AccountCompanion, Multiselect },
  data() {
    let options = Object.entries(genderOptions).map(o => {
      let [code, label] = o;
      return { code, label };
    });
    return {
      userRoles,
      frequentflyerReady: false,
      userReady: false,
      frequentflyer: {},
      user: {},
      dobText: "",
      accountSavedDisplay: false,
      subscriptionCancelled: false,
      cancelPlanProgress: false,
      genderOptions: options
    };
  },
  watch: {
    userReady(val) {
      if (!val) return;
      this.$nextTick(() => {
        const that = this;
        new Lightpick({
          field: this.$refs.dob,
          onSelect(value) {
            that.setDOB(value);
          }
        });
      });
    }
  },
  created() {
    api.get("/users/me/frequentflyer/").then(response => {
      this.frequentflyer = response.data;
      this.frequentflyerReady = true;
    });
    api.get("/users/me/").then(response => {
      this.user = response.data;
      this.userReady = true;
      this.dobText = formatDateFull(moment(this.user.dob));
    });
  },
  methods: {
    ...Vuex.mapActions("user", ["initializeUser"]),
    planStatus(plan) {
      if (
        !(this.user && this.user.subscription && this.user.subscription.plan)
      ) {
        return null;
      }
      const planOrder = ["basic", "premium"];
      const currentPlanIndex = planOrder.indexOf(this.user.subscription.plan);
      const planIndex = planOrder.indexOf(plan);
      if (planIndex < currentPlanIndex) return "downgrade";
      if (planIndex === currentPlanIndex) return "current";
      if (planIndex > currentPlanIndex) return "upgrade";
    },
    updateHomeAirport(value) {
      this.user.market = value;
    },
    setDOB(value) {
      this.user.dob = value.format().slice(0, 10);
    },
    saveFrequentFlyer() {
      api
        .patch("/users/me/frequentflyer/", this.frequentflyer)
        .then(response => {
          this.frequentflyer = response.data;
        });
    },
    saveAccount() {
      api.patch("/users/me/", this.user).then(response => {
        this.user = { ...this.user, ...response.data };
        this.dobText = this.user.dob
          ? moment(this.user.dob).format("MM/DD/YYYY")
          : "";
        this.accountSavedDisplay = true;
        setTimeout(() => {
          this.accountSavedDisplay = false;
        }, 5000);
      });
    },
    cancelPlan() {
      if (this.cancelPlanProgress) return;
      this.cancelPlanProgress = true;
      api
        .post("subscriptions/cancel-subscription/")
        .then(() => {
          this.initializeUser().then(() => {
            this.subscriptionCancelled = true;
          });
        })
        .finally(() => {
          this.cancelPlanProgress = false;
        });
    },
    goToOverview() {
      this.$router.push({ name: "dashboard-ui-overview" });
    },
    airlineIcon
  },
  computed: {
    ...Vuex.mapState("plans", ["plans"]),
    frequentFlyerNames() {
      return frequentFlyerNames;
    },
    airlineCodes() {
      return airlineCodes;
    }
  }
};
</script>

<style lang="scss">
.account-view {
  margin-top: 2rem;

  .account-view-container {
    width: 73%;
    margin-left: calc(14% - 70px);
  }
  .account-box {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    margin: 0 1% 2rem 1%;
    padding: 1rem 1.25rem 1.25rem 1rem;
    max-width: 48%;

    .box-header {
      font-family: Dona-Bold;
      font-size: 1rem;
      line-height: 1.25rem;
      color: black;
    }

    hr {
      margin: 0 0.5rem 1rem -0.7rem;
      border-top: 1px solid #979797;
      width: 103%;
    }

    .row-form {
      display: flex;
      align-items: center;
      margin-bottom: 0.75rem;

      & > * {
        width: 49%;
        margin-right: 1.25rem;
      }
    }

    input.row-form-input {
      background: #eaeaea;
      font-family: Dona-Regular;
      font-size: 0.75rem;
      line-height: 1rem;
      padding: 0.75rem 1.25rem 0.5rem 0.75rem;
      margin-right: 1.25rem;
      outline: none;
      border: 1px solid transparent;
      flex-grow: 1;
      min-width: 0;

      &:focus {
        background: #fafafa;
        border: 1px solid #979797;
      }
    }

    input.full-width-input {
      width: 100%;
    }

    .multiselect__tags {
      padding: 0px 40px 0 8px;
      background-color: #eaeaea;
      border: none;
      min-height: 39px;

      & > span,
      & > input {
        font-size: 13px;
        margin-top: 10px;
        margin-bottom: 0;
        padding-top: 0;
        padding-left: 5px;
        color: $gray-700;
        background-color: #eaeaea;
      }
    }

    button {
      width: 100%;
      font-family: Dona-Bold;
      font-size: 0.9rem;
      line-height: 1.25rem;
      padding-top: 0.6rem;
      padding-bottom: 0.35rem;
      color: black;
      background: white;
      border: 1px solid #00aeef;
      border-radius: 4px;
      outline: none;
    }

    &.deal-alert-notification {
      .row-form {
        .dest-input {
          width: 35%;
        }

        .air-lines-input {
          margin-right: 0;
        }

        .max-price-input {
          width: 25%;
        }
      }
    }

    &.additional-users {
      .row-form {
        width: 70%;
        button {
          font-size: 0.75rem;
          line-height: 1rem;
        }
      }
    }
  }
  .account-box-container {
    max-width: 48%;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
    padding: 1rem 1.25rem 1.25rem 1rem;
    margin: 0 1% 2rem 1%;
    background-color: white;

    .subscription-management {
      justify-content: space-between;
      padding: 1rem;

      .subscription-wrapper {
        flex: 0 0 49%;
        width: 49%;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border: none;
        padding: 1.5rem 0.5rem;

        .subscription {
          border: none;
          padding: 0;

          .subscription__heading {
            font-size: 1rem;
            font-family: Dona-Bold;
            text-align: center;
            color: black;
          }
          .subscription__list {
            text-align: center;

            .subscription__item {
              color: #8d8d8d;
              font-size: 0.75rem;
              font-family: Dona-Regular;
            }
          }
          .subscription__bottom {
            .button--outline-blue {
              width: 100%;
              font-family: Dona-Bold;
              font-size: 0.9rem;
              line-height: 1.25rem;
              padding-top: 0.6rem;
              padding-bottom: 0.35rem;
              color: black;
              background: white;
              border: 1px solid #00aeef;
              border-radius: 4px;
              outline: none;
            }
          }
        }
      }
    }
    & > h3 {
      font-family: Dona-Bold;
      font-size: 1rem;
      line-height: 1.25rem;
      color: black;
    }
    & > hr {
      margin: 0 0.5rem 1rem -0.7rem;
      border-top: 1px solid #979797;
      width: 103%;
    }
  }
}
</style>
