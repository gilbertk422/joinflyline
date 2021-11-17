<template>
  <div class="dashboard-overview">
    <modal
      :showCloseButton="false"
      v-show="user.subscription === null"
      @close="showModal = false"
      @click-outside="showModal = false"
    >
      <template slot="body">
        <MembershipGuest />
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

    <div class="row dashboard">
      <div class="col-3 offset-1 info-section" v-if="trip_summary">
        <div class="section-container">
          <div class="dash-box trips-taken">
            <h4 class="box-header">Trips Taken</h4>
            <hr />
            <div class="box-body">
              <div>
                <label>{{ trip_summary.count.domestic }}</label>
                <span>Domestic</span>
              </div>
              <div>
                <label>{{ trip_summary.count.international }}</label>
                <span>International</span>
              </div>
            </div>
          </div>
          <div class="dash-box estimated-saving">
            <h4 class="box-header">Estimated Savings</h4>
            <hr />
            <div class="box-body">
              <label
                >${{
                  trip_summary.savings.domestic +
                    trip_summary.savings.international
                }}</label
              >
              <span>Savings</span>
            </div>
          </div>
          <div class="dash-box popular-dest">
            <h4 class="box-header">Popular Destinations</h4>
            <hr />
            <div class="box-body">
              <label v-for="rdeal in randomDeals" :key="rdeal.id"
                >- {{ rdeal.city_to_name }} ({{ rdeal.fly_to }})</label
              >
            </div>
          </div>
          <div class="dash-box popular-dest">
            <h4 class="box-header">Trending Trips</h4>
            <hr />
            <div class="box-body" v-if="userDeals">
              <label v-for="rdeal in userDeals" :key="rdeal.id"
                >- {{ rdeal.city_from_name }} ({{ rdeal.fly_from }}) ->
                {{ rdeal.city_to_name }} ({{ rdeal.fly_to }})</label
              >
            </div>
          </div>
        </div>
      </div>
      <div class="col-4 feed-section">
        <div class="dash-box">
          <h4 class="box-header">Deal Feed</h4>
          <hr />
          <div class="box-body">
            <deal v-for="rdeal in feedDeals" :deal="rdeal" :key="rdeal.id" />
          </div>
        </div>
      </div>
      <div class="col-3 filter-section">
        <div class="section-container">
          <div class="dash-box">
            <h4 class="box-header">Deal Filters</h4>
            <hr />
            <!--
            <div class="check-item">
              <input
                class="filter-checkbox"
                type="checkbox"
                id="domestic-deal"
                :checked="locationFilter === 'domestic'"
                @change="toggleLocationFilter('domestic')"
              />
              <label for="domestic-deal">Domestic Deals</label>
            </div>
            <div class="check-item">
              <input
                class="filter-checkbox"
                type="checkbox"
                id="international-deal"
                :checked="locationFilter === 'international'"
                @change="toggleLocationFilter('international')"
              />
              <label for="international-deal">International Deals</label>
            </div>
            <hr />
            -->
            <div class="check-item" v-for="p in airlineFilters" :key="p[0]">
              <input
                class="filter-checkbox"
                type="checkbox"
                :checked="p[1]"
                @change="toggleAirline(p[0])"
                :id="`airline-filter-${p[0]}`"
              />
              <label :for="`airline-filter-${p[0]}`">{{
                airlineCodes[p[0]]
              }}</label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vuex from "vuex";
import api from "../../utils/http";
import { formatDateDeals } from "../../utils/utils";
import Deal from "../Deal";
import { airlineCodes } from "../../utils/airlineCodes";
import MembershipGuest from "../MembershipGuest";

export default {
  name: "DashboardUiOverview",
  data() {
    return {
      trip_summary: null,
      airlineCodes
    };
  },
  components: {
    Deal,
    MembershipGuest
  },
  methods: {
    formatDateDeals,
    ...Vuex.mapActions("deals", ["toggleAirline", "toggleLocationFilter"])
  },
  created() {
    api.get("/bookings/summary/").then(response => {
      this.trip_summary = response.data;
    });
  },
  computed: {
    ...Vuex.mapState("user", ["user"]),
    ...Vuex.mapState("deals", [
      "userDeals",
      "randomDeals",
      "feedDeals",
      "locationFilter"
    ]),
    ...Vuex.mapGetters("deals", ["airlineFilters"])
  }
};
</script>

<style lang="scss">
.dash-box {
  background: #ffffff;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
  padding: 1rem;
  width: 100%;
  margin-bottom: 0.875rem;

  .box-header {
    font-family: Dona-Bold;
    font-size: 0.875rem;
    line-height: 1rem;
    color: #000000;
  }

  hr {
    margin: 0 0.5rem 0.5rem -0.5rem;
    border-top: 1px solid #d8d8d8;
  }
}

.section-container {
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
  overflow-y: auto;
  max-height: calc(100vh - 160px);
}
.section-container::-webkit-scrollbar {
  display: none; /* Safari and Chrome */
}

.dashboard-overview {
  margin-top: 2rem;
  .dashboard {
    margin-top: 2rem;
    -ms-overflow-style: none; /* Internet Explorer 10+ */
    scrollbar-width: none; /* Firefox */
    overflow: auto;

    .trips-taken {
      .box-body {
        display: flex;
        justify-content: center;
        div {
          display: flex;
          justify-content: flex-start;
          align-items: flex-end;
          width: 50%;
          padding-top: 0.5rem;
          &:first-child {
            border-right: 1px solid #d8d8d8;
          }

          label {
            font-family: Dona-Regular;
            font-weight: bold;
            font-size: 3.125rem;
            line-height: 3.5rem;
            margin-bottom: 0;
            margin-left: 1rem;
            margin-right: 0.5rem;
            color: #000000;
          }
          span {
            font-family: Dona-Regular;
            font-weight: bold;
            font-size: 0.75rem;
            line-height: 0.875rem;
            color: #9d9d9d;
            margin-bottom: 1rem;
          }
        }
      }
    }

    .estimated-saving {
      .box-body {
        padding-top: 0.5rem;
        label {
          font-family: Dona-Regular;
          font-weight: bold;
          font-size: 2.5rem;
          line-height: 2.875rem;
          color: #000000;
          margin-bottom: 0;
        }

        span {
          margin-left: 0.5rem;
          font-family: Dona-Regular;
          font-weight: bold;
          font-size: 0.75rem;
          line-height: 1.125rem;
          color: #9d9d9d;
        }
      }
    }

    .popular-dest {
      .box-body {
        label {
          font-family: Dona-Regular;
          font-style: normal;
          font-weight: bold;
          font-size: 0.8rem;
          line-height: 1.875rem;
          color: #9d9d9d;
          display: block;
        }
      }
    }

    .feed-section {
      font-family: Dona-Regular;
      .dash-box {
        .box-header {
          font-weight: bold;
          font-size: 1.375rem;
          line-height: 1.5rem;
        }
        hr {
          margin: 0.5rem -0.75rem;
        }

        .feed-item {
          display: flex;
          padding-bottom: 0.5rem;
          padding-top: 0.5rem;
          border-bottom: 1px solid #d8d8d8;

          .feed-logo {
            width: 6.25rem;
            height: 6.25rem;
          }

          .feed-info {
            margin-left: 1rem;
            flex-grow: 1;
            .feed-title {
              font-family: dona-bold;
              font-size: 0.8rem;
              line-height: 1.125rem;
              color: #000000;
              margin-bottom: 0.45rem;
            }

            p {
              font-weight: bold;
              font-size: 0.7rem;
              line-height: 0.875rem;
              color: #9d9d9d;
              margin-bottom: 0.45rem;
            }

            .feed-order {
              display: flex;
              justify-content: space-between;
              margin-bottom: 0.5rem;
              div {
                display: flex;
                img {
                  width: 1.2rem;
                  height: 1.2rem;
                  margin-right: 0.225rem;
                }
              }

              button {
                font-family: dona-bold;
                font-size: 0.8rem;
                line-height: 1.25rem;
                text-align: center;
                color: #ffffff;
                background: #00aeef;
                border: 1.2px solid #00aeef;
                border-radius: 4px;
                padding: 0.375rem 0.75rem;
              }
            }
          }
        }
      }
    }

    .filter-section {
      font-family: Dona-Regular;
      font-size: 0.8rem;
      color: #9d9d9d;
      position: sticky;
      top: 0;
      display: table;
      .dash-box {
        .box-header {
          font-weight: bold;
          font-size: 1.375rem;
          line-height: 1.5rem;
        }
        hr {
          margin: 1rem -0.75rem;
        }

        .check-item {
          .filter-checkbox {
            position: absolute; // take it out of document flow
            opacity: 0; // hide it

            & + label {
              position: relative;
              cursor: pointer;
              padding: 0;
            }

            // Box.
            & + label:before {
              content: "";
              margin-right: 10px;
              display: inline-block;
              vertical-align: text-bottom;
              width: 20px;
              height: 20px;
              border-radius: 4px;
              border: 1.2px solid #b8b8b8;
              background: white;
            }

            // Box hover
            &:hover + label:before {
              background: #00aeef;
            }

            // Box focus
            &:focus + label:before {
              box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.12);
            }

            // Box checked
            &:checked + label:before {
              background: #00aeef;
            }

            // Disabled state label.
            &:disabled + label {
              color: #b8b8b8;
              cursor: auto;
            }

            // Disabled box.
            &:disabled + label:before {
              box-shadow: none;
              background: #ddd;
            }

            // Checkmark. Could be replaced with an image
            &:checked + label:after {
              content: "";
              position: absolute;
              left: 5px;
              top: 9px;
              background: white;
              width: 2px;
              height: 2px;
              box-shadow: 2px 0 0 white, 4px 0 0 white, 4px -2px 0 white,
                4px -4px 0 white, 4px -6px 0 white, 4px -8px 0 white;
              transform: rotate(45deg);
            }
          }
        }
      }
    }

    .info-section {
      position: sticky;
      top: 0;
      display: table;
    }
  }
  .dashboard::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
  }
}
</style>
