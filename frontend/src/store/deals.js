import api from "../utils/http";

const filterAirlines = [
  "AA",
  "AF",
  "AK",
  "AS",
  "B6",
  "BA",
  "CA",
  "CX",
  "DL",
  "EK",
  "F9",
  "FR",
  "KL",
  "QF",
  "QR",
  "SQ",
  "U2",
  "UA",
  "WN"
];

export const dealsStore = {
  namespaced: true,
  state: {
    randomDeals: null,
    userDeals: null,
    feedDeals: null,
    randomDealsRetrieveError: false,
    userDealsRetrieveError: false,
    feedDealsRetrieveError: false,
    selectedAirlines: new Set(),
    locationFilter: null
  },
  mutations: {
    SELECT_AIRLINE(state, value) {
      state.selectedAirlines.add(value);
    },
    DESELECT_AIRLINE(state, value) {
      state.selectedAirlines.delete(value);
    },
    TOGGLE_AIRLINE(state, airline) {
      if (state.selectedAirlines.has(airline)) {
        state.selectedAirlines.delete(airline);
      } else {
        state.selectedAirlines.add(airline);
      }
    },
    SET_LOCATION_FILTER(state, value) {
      state.locationFilter = value;
    },
    RESET_FILTERS(state) {
      state.selectedAirlines = new Set();
      state.locationFilter = null;
    },
    SET_RANDOM_DEALS(state, value) {
      state.randomDeals = value;
    },
    SET_USER_DEALS(state, value) {
      state.userDeals = value;
    },
    SET_RANDOM_DEALS_RETRIEVE_ERROR(state, value) {
      state.randomDealsRetrieveError = value;
    },
    SET_USER_DEALS_RETRIEVE_ERROR(state, value) {
      state.userDealsRetrieveError = value;
    },
    SET_FEED_DEALS(state, value) {
      state.feedDeals = value;
    },
    SET_FEED_DEALS_RETRIEVE_ERROR(state, value) {
      state.feedDealsRetrieveError = value;
    },
    RESET(state) {
      state.userDealsRetrieveError = false;
      state.userDeals = null;
    }
  },
  actions: {
    toggleLocationFilter(context, value) {
      if (context.state.locationFilter === value) {
        context.commit("SET_LOCATION_FILTER", null);
      } else {
        context.commit("SET_LOCATION_FILTER", value);
      }
      context.dispatch("fetchFeedDeals");
    },
    toggleAirline(context, value) {
      context.commit("TOGGLE_AIRLINE", value);
      context.dispatch("fetchFeedDeals");
    },
    reset(context) {
      context.commit("RESET");
    },
    fetchRandomDeals(context) {
      api
        .get("/deals/")
        .then(response => {
          context.commit("SET_RANDOM_DEALS", response.data.results);
          context.commit("SET_RANDOM_DEALS_RETRIEVE_ERROR", false);
        })
        .catch(() => {
          context.commit("SET_RANDOM_DEALS_RETRIEVE_ERROR", true);
        });
    },
    fetchFeedDeals(context) {
      let params = { size: 40 };
      if (context.state.locationFilter) {
        params.kind = context.state.locationFilter;
      }
      if (context.state.selectedAirlines.size > 0) {
        params.airlines = [...context.state.selectedAirlines].join(",");
      }
      api
        .get("/deals/", {
          params
        })
        .then(response => {
          context.commit("SET_FEED_DEALS", response.data.results);
          context.commit("SET_FEED_DEALS_RETRIEVE_ERROR", false);
        })
        .catch(() => {
          context.commit("SET_FEED_DEALS_RETRIEVE_ERROR", true);
        });
    },
    fetchUserDeals(context, user) {
      if (user.anonymous) return;
      api
        .get("/deals/", {
          params: {
            city_from: `${user.market.type}:${user.market.code}`
          }
        })
        .then(response => {
          context.commit("SET_USER_DEALS", response.data.results);
          context.commit("SET_USER_DEALS_RETRIEVE_ERROR", false);
        })
        .catch(() => {
          context.commit("SET_USER_DEALS_RETRIEVE_ERROR", true);
        });
    }
  },
  getters: {
    airlineFilters(state) {
      return filterAirlines.map(e => [e, state.selectedAirlines.has(e)]);
    }
  }
};
