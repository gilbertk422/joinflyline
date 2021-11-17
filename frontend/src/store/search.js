import {
  getQuickLinksData,
  processFlight,
  getAirlines,
  getStops,
  getSearchParams
} from "../utils/utils";

import {
  airlineCodes,
  lowcostAirlines,
  legacyAirlines
} from "../utils/airlineCodes";

import moment from "moment";
import api from "../utils/http";
import { sleep } from "../utils/utils";

function initialTimeFilters() {
  return {
    departure: {
      takeoff: [0, 24 * 60],
      landing: [0, 24 * 60]
    },
    return: {
      takeoff: [0, 24 * 60],
      landing: [0, 24 * 60]
    }
  };
}

const scrapers = ["skyscanner"];

export const searchStore = {
  namespaced: true,
  state: {
    authErrorText: "",
    plans: null,
    form: {
      email: "",
      airlinesFilter: null,
      limit: 10,
      limitIncrement: 0,
      sort: "price",
      priceRange: [0, 3000],
      airlines: [],
      maxStops: null,
      destinationTypeId: "round",
      searchType: "searchNBook",
      seatType: "M",
      valAdults: 1,
      valChildren: 0,
      valInfants: 0,
      departure_date: "",
      return_date: "",
      departure_date_data: null,
      return_date_data: null,
      placeFrom: null,
      placeTo: null,
      singleCarrier: false,
      timeFilters: initialTimeFilters(),
      isDeals: false
    },
    searchResults: [],
    searchProgress: false,
    searchResultIndex: null,
    showDashboardNavigation: true,
    dealAlertsSubscribeProgress: false,
    dealAlertsSubscribeSuccess: false,
    dealAlertsSubscribeFailure: false,
    scraperTaskIds: {},
    scraperResults: {}
  },
  mutations: {
    REMOVE_SCRAPER(state, v) {
      state.scraperTaskIds = {
        ...Object.entries(state.scraperTaskIds).filter(o => o[0] !== v)
      };
    },
    SET_SCRAPER_TASK_ID(state, v) {
      state.scraperTaskIds = { ...state.scraperTaskIds, ...v };
    },
    SET_SCRAPER_RESULT(state, v) {
      state.scraperResults = { ...state.scraperResults, ...v };
    },
    RESET_SCRAPERS(state) {
      state.scraperTaskIds = {};
      state.scraperResults = {};
      state.pollActive = false;
    },
    SET_DEAL_ALERTS_SUBSCRIBE_SUCCESS(state, v) {
      state.dealAlertsSubscribeSuccess = v;
    },
    SET_DEAL_ALERTS_SUBSCRIBE_FAILURE(state, v) {
      state.dealAlertsSubscribeFailure = v;
    },
    SET_EMAIL(state, v) {
      state.form.email = v;
    },
    SET_TIME_FILTERS(state, v) {
      const { destination, direction, value } = v;
      state.form.timeFilters[destination][direction] = value;
    },
    RESET_TIME_FILTERS(state) {
      state.form.timeFilters = initialTimeFilters();
    },
    SET_SINGLE_CARRIER(state) {
      state.form.singleCarrier = true;
    },
    TOGGLE_SINGLE_CARRIER(state) {
      state.form.singleCarrier = !state.form.singleCarrier;
    },
    setQuickFiltersData(state, value) {
      state.quickFiltersData = value;
    },
    setSearchResults(state, results) {
      state.searchResults = results;
    },
    updatePlaceFrom(state, value) {
      state.form.placeFrom = value;
    },
    updatePlaceTo(state, value) {
      state.form.placeTo = value;
    },
    clearFilters(state) {
      for (let a of state.form.airlines) {
        a.checked = false;
      }
      state.form.maxStops = null;
      state.form.limitIncrement = 0;
    },
    setMaxStops(state, value) {
      state.form.maxStops = value;
    },
    setSeatType(state, value) {
      state.form.seatType = value;
    },
    setPriceRange(state, value) {
      state.form.priceRange = value;
    },
    toggleAirline(state, index) {
      state.form.airlines[index].checked = !state.form.airlines[index].checked;
    },
    setDestinationType(state, value) {
      state.form.destinationTypeId = value;
    },
    setSearchType(state, value) {
      state.form.searchType = value;
    },
    increaseLimit(state, by) {
      state.form.limitIncrement += by;
    },
    toggleSort(state, value) {
      if (state.form.sort === value) {
        state.form.sort = null;
      } else {
        state.form.sort = value;
      }
    },
    setDates(state, payload) {
      const { start, end } = payload;
      if (start) state.form.departure_date = start.format("MM/DD/YYYY");
      if (end) state.form.return_date = end.format("MM/DD/YYYY");
      state.form.departure_date_data = start;
      state.form.return_date_data = end;
    },
    updatePassengers(state, payload) {
      const { index, by } = payload;
      let vals = {
        valAdults: state.form.valAdults,
        valChildren: state.form.valChildren,
        valInfants: state.form.valInfants
      };
      const propertyName = ["valAdults", "valChildren", "valInfants"][
        index - 1
      ];
      vals[propertyName] += by;
      const passengers = vals.valAdults + vals.valChildren + vals.valInfants;
      if (!(passengers > 0 && passengers <= 9)) return;
      if (vals.valInfants > vals.valAdults) return;
      if (vals.valInfants > 0 && vals.valChildren > 0 && vals.valAdults === 0)
        return;
      state.form = { ...state.form, ...vals }; // Apply changes
    },
    setSearchProgress(state, value) {
      state.searchProgress = value;
    },
    setSearchResultIndex(state, value) {
      state.searchResultIndex = value;
    },
    setAirlines(state, value) {
      state.form.airlines = value;
    },
    setPlans(state, value) {
      state.plans = value;
    },
    resetAirlinesFilter(state) {
      state.form.airlinesFilter = null;
    },
    toggleAirlinesFilter(state, value) {
      if (state.form.airlinesFilter === value) {
        state.form.airlinesFilter = null;
      } else {
        state.form.airlinesFilter = value;
      }
    },
    setAuthError(state, value) {
      state.authErrorText = value;
    },
    showDashboardNav(state) {
      state.showDashboardNavigation = true;
    },
    hideDashboardNav(state) {
      state.showDashboardNavigation = false;
    },
    setForm(state, data) {
      state.form = {
        ...state.form,
        placeFrom: data.place_from,
        placeTo: data.place_to,
        valAdults: data.adults,
        valChildren: data.children,
        valInfants: data.infants,
        seatType: data.seat_type,
        destinationTypeId: data.destination_type
      };
    }
  },
  actions: {
    setDealAlertsSubscribeSuccess(context, value) {
      context.commit("SET_DEAL_ALERTS_SUBSCRIBE_SUCCESS", value);
    },
    setDealAlertsSubscribeFailure(context, value) {
      context.commit("SET_DEAL_ALERTS_SUBSCRIBE_FAILURE", value);
    },
    setEmail(context, value) {
      context.commit("SET_EMAIL", value);
    },
    toggleSingleCarrier(context) {
      context.commit("TOGGLE_SINGLE_CARRIER");
    },
    setSingleCarrier(context, value) {
      context.commit("SET_SINGLE_CARRIER", value);
    },
    setTimeFilters(context, value) {
      context.commit("SET_TIME_FILTERS", value);
    },
    setFormAndSearch(context, data) {
      context.commit("setForm", data);
      const departureDate = moment(data.departure_date);
      const returnDate = data.return_date ? moment(data.return_date) : null;
      context.commit("setDates", { start: departureDate, end: returnDate });
      context.dispatch("search", { clearFilters: true, saveSearch: false });
    },
    applyAirlinesFilter(context, kind) {
      context.commit("toggleAirlinesFilter", kind);
    },
    loadMore(context) {
      context.commit("increaseLimit", 10);
    },
    sortResultsBy(context, sort) {
      context.commit("toggleSort", sort);
    },
    clearFiltersAndUpdate(context) {
      context.commit("clearFilters");
      context.commit("setPriceRange", [
        context.getters.priceLimits.min,
        context.getters.priceLimits.max
      ]);
      context.commit("resetAirlinesFilter");
      context.commit("RESET_TIME_FILTERS");
    },
    anonymousDealAlertsSubscribe(context) {
      const { placeFrom, placeTo, email } = context.state.form;
      api
        .post("deal-alert-subscribe/", {
          source: placeFrom,
          destination: placeTo,
          email: email
        })
        .then(() => {
          context.commit("SET_DEAL_ALERTS_SUBSCRIBE_SUCCESS", true);
        })
        .catch(() => {
          context.commit("SET_DEAL_ALERTS_SUBSCRIBE_FAILURE", true);
        });
    },
    search(context, payload) {
      const { saveSearch } = payload;
      context.commit("setSearchResultIndex", null);
      context.commit("setSearchProgress", true);
      context.commit("RESET_SCRAPERS");
      api
        .get("search/", { params: getSearchParams(context.state.form) })
        .then(response => {
          const data = response.data;
          let parent = { ...data };
          delete parent.data;
          data.data = data.data.map(processFlight);
          data.data = data.data.map((o, i) => {
            o.parent = parent;
            o.provider = "flyline";
            o.srIndex = `kiwi-${i}`;
            Object.freeze(o);
            return o;
          });
          const airlines = getAirlines(data.data);
          context.commit(
            "setAirlines",
            airlines.map((a, i) => ({
              code: a,
              name: airlineCodes[a] || a,
              checked: false,
              aIndex: i
            }))
          );
          context.commit("setSearchResults", data.data);
          context.commit("setPriceRange", [
            context.getters.priceLimits.min,
            context.getters.priceLimits.max
          ]);
        })
        .finally(() => {
          context.commit("setSearchProgress", false);
        });
      if (!context.rootState.user.anonymous) {
        context.dispatch("requestScrapers", {
          fly_from: context.state.form.placeFrom.code,
          fly_to: context.state.form.placeTo.code,
          start_date: context.state.form.departure_date_data.format(
            "YYYY-MM-DD"
          ),
          return_date: context.state.form.return_date_data.format("YYYY-MM-DD")
        });
      }
      if (saveSearch) {
        context.dispatch("saveSearchHistory");
      }
    },
    requestScrapers(context, request) {
      let promises = [sleep(1000)];
      for (const kind of scrapers) {
        const p = api
          .post("/request-scraper/", {
            kind: kind,
            ...request
          })
          .then(response => {
            context.commit("SET_SCRAPER_TASK_ID", {
              [kind]: response.data.id
            });
          });
        promises.push(p);
      }
      Promise.allSettled(promises).then(() => {
        context.dispatch("pollScrapers");
      });
    },
    pollScrapers(context) {
      if (Object.entries(context.state.scraperTaskIds).length === 0) return;
      let promises = [sleep(2000)];
      for (const [scraper, taskId] of Object.entries(
        context.state.scraperTaskIds
      )) {
        if (context.state.scraperResults[scraper]) continue;
        const p = api
          .get("/check-scraper-result/", { params: { id: taskId } })
          .then(response => {
            const data = response.data.map(processFlight).map((o, i) => {
              o.srIndex = `${scraper}-${i}`;
              o.provider = scraper;
              Object.freeze(o);
              return o;
            });
            context.commit("SET_SCRAPER_RESULT", { [scraper]: data });
            context.commit("REMOVE_SCRAPER", scraper);
            context.commit("setPriceRange", [
              context.getters.priceLimits.min,
              context.getters.priceLimits.max
            ]);
          })
          .catch(error => {
            if (
              error &&
              error.response &&
              error.response.data &&
              error.response.data.status === "not-ready"
            )
              return;
            context.commit("REMOVE_SCRAPER", scraper);
          });
        promises.push(p);
      }
      Promise.allSettled(promises).then(() => {
        context.dispatch("pollScrapers");
      });
    },
    saveSearchHistory(context) {
      api.post("/search-history/", {
        place_from: context.state.form.placeFrom,
        place_to: context.state.form.placeTo,
        departure_date: context.state.form.departure_date_data
          .toJSON()
          .slice(0, 10),
        return_date: context.state.form.return_date_data
          ? context.state.form.return_date_data.toJSON().slice(0, 10)
          : null,
        adults: context.state.form.valAdults,
        children: context.state.form.valChildren,
        infants: context.state.form.valInfants,
        seat_type: context.state.form.seatType,
        destination_type: context.state.form.destinationTypeId
      });
    }
  },
  getters: {
    isDealFormIncomplete(state) {
      return !(
        !!state.form.placeFrom &&
        !!state.form.placeTo &&
        !!state.form.email
      );
    },
    email(state) {
      return state.form.email;
    },
    quickFiltersData(state, getters) {
      return getQuickLinksData(getters.filteredResults);
    },
    filterableAirlines(state, getters) {
      const kind = state.form.airlinesFilter;
      let result;
      if (kind === "lowcost") {
        result = state.form.airlines.filter(o =>
          lowcostAirlines.includes(o.code)
        );
      } else if (kind === "legacy") {
        result = state.form.airlines.filter(o =>
          legacyAirlines.includes(o.code)
        );
      } else {
        result = state.form.airlines;
      }
      if (state.form.singleCarrier) {
        const singleCarrierAirlines = new Set(
          getters.allResults
            .filter(o => o.airlines.length === 1)
            .map(o => o.airlines[0])
        );
        result = result.filter(o => singleCarrierAirlines.has(o.code));
      }
      return result;
    },
    checkedAirlines(state, getters) {
      return getters.filterableAirlines.filter(o => o.checked).map(o => o.code);
    },
    airlinesFilterToApply(state, getters) {
      const kind = state.form.airlinesFilter;
      if (getters.checkedAirlines.length > 0) {
        return getters.checkedAirlines;
      }
      if (kind === "lowcost") {
        return lowcostAirlines;
      } else if (kind === "legacy") {
        return legacyAirlines;
      }
      return [];
    },
    allResults(state) {
      return [
        ...state.searchResults,
        ...Object.values(state.scraperResults).flat()
      ];
    },
    filteredResults(state, getters) {
      let result = getters.allResults;
      if (getters.airlinesFilterToApply.length > 0) {
        result = result.filter(o => {
          return o.airlines.every(a =>
            getters.airlinesFilterToApply.includes(a)
          );
        });
      }
      result = result.filter(o => {
        return (
          o.price >= state.form.priceRange[0] &&
          o.price <= state.form.priceRange[1]
        );
      });
      if (state.form.maxStops !== null) {
        result = result.filter(o => {
          return getStops(o) <= state.form.maxStops;
        });
      }
      result = result.filter(o => {
        const tf = state.form.timeFilters;
        if (o.roundtrip) {
          if (
            o.local_departure_int < tf.departure.takeoff[0] ||
            o.local_departure_int > tf.departure.takeoff[1]
          )
            return false;
          if (
            o.local_arrival_int < tf.departure.landing[0] ||
            o.local_arrival_int > tf.departure.landing[1]
          )
            return false;
          if (
            o.return_departure_int < tf.return.takeoff[0] ||
            o.return_departure_int > tf.return.takeoff[1]
          )
            return false;
          if (
            o.return_arrival_int < tf.return.landing[0] ||
            o.return_arrival_int > tf.return.landing[1]
          )
            return false;
          return true;
        } else {
          if (
            o.local_departure_int < tf.departure.takeoff[0] ||
            o.local_departure_int > tf.departure.takeoff[1]
          )
            return false;
          if (
            o.return_arrival_int < tf.return.landing[0] ||
            o.return_arrival_int > tf.return.landing[1]
          )
            return false;
          return true;
        }
      });
      if (state.form.singleCarrier) {
        result = result.filter(o => o.airlines.length === 1);
      }
      if (state.form.sort) {
        if (state.form.sort === "price") {
          result.sort((a, b) => {
            if (a.price > b.price) return 1;
            if (a.price === b.price) {
              if (a.quality > b.quality) return 1;
              if (a.quality === b.quality) return 0;
              if (a.quality < b.quality) return -1;
            }
            return -1;
          });
        } else if (state.form.sort === "quality") {
          result.sort((a, b) => {
            if (a.quality > b.quality) return 1;
            if (a.quality === b.quality) {
              if (a.price > b.price) return 1;
              if (a.price === b.price) return 0;
              return -1;
            }
            return -1;
          });
        } else if (state.form.sort === "duration") {
          result.sort((a, b) => {
            const adur = Math.min(
              ...[a.duration.departure, a.duration.return].filter(o => o)
            );
            const bdur = Math.min(
              ...[b.duration.departure, b.duration.return].filter(o => o)
            );
            if (adur > bdur) return 1;
            if (adur === bdur) {
              if (a.price > b.price) return 1;
              if (a.price === b.price) return 0;
              return -1;
            }
            return -1;
          });
        }
      }
      return result;
    },
    priceLimits(state, getters) {
      const prices = getters.allResults.map(o => o.price);
      return {
        min: Math.min(...prices),
        max: Math.max(...prices)
      };
    },
    finalResults(state, getters, rootState, rootGetters) {
      const limit = rootGetters["user/user"].anonymous
        ? 4
        : state.form.limit + state.form.limitIncrement;
      return getters.filteredResults.slice(0, limit);
    },
    cityFromTo(state) {
      if (!state.form.placeFrom || !state.form.placeTo) {
        return null;
      }
      return `${state.form.placeFrom.name} -> ${state.form.placeTo.name}`;
    },
    airlineNames(state) {
      if (!(state.form.airlines && state.form.airlines.length > 0)) return null;
      const airlines = state.form.airlines.map(o => o.name);
      const others = airlines.length - 3;
      const airlinesText = airlines.slice(0, 3).join(", ");
      if (others > 0) {
        return `${airlinesText} and ${others} more`;
      }
      return airlinesText;
    },
    flightToBook(state) {
      if (state.searchResultIndex === null) return null;
      const [provider, index] = state.searchResultIndex.split("-");
      const i = parseInt(index);
      if (provider === "kiwi") {
        return state.searchResults[i];
      } else {
        return state.scraperResults[provider][i];
      }
    },
    isDomestic(state, getters) {
      return (
        getters.flightToBook.countryFrom.code ===
        getters.flightToBook.countryTo.code
      );
    },
    returnFlights(state, getters) {
      return getters.flightToBook
        ? getters.flightToBook.route.filter(o => o.return === 1)
        : [];
    },
    departureFlights(state, getters) {
      return getters.flightToBook
        ? getters.flightToBook.route.filter(o => o.return === 0)
        : [];
    },
    singleCarrierAirlines(state, getters) {
      const singleCarrierAirlines = new Set(
        getters.allResults
          .filter(o => o.airlines.length === 1)
          .map(o => o.airlines[0])
      );
      return [...singleCarrierAirlines];
    }
  }
};
