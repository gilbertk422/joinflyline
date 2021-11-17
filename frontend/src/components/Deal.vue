<template>
  <div class="feed-item">
    <img class="feed-logo" :src="getCityThumbnail(deal.fly_to)" />
    <div class="feed-info">
      <h4 class="feed-title">
        {{ deal.city_from_name }} ({{ deal.fly_from }}) -
        {{ deal.city_to_name }} ({{ deal.fly_to }})
      </h4>
      <p class="feed-date">
        {{ formatDateDeals(deal.departure_date) }} -
        {{ formatDateDeals(deal.return_date) }}
      </p>
      <p class="feed-type">Round-trip</p>
      <div class="feed-order">
        <div>
          <img
            :src="airlineIcon(airline)"
            v-for="airline in deal.airlines"
            :key="`deal-${deal.id}-${airline}`"
          />
        </div>
        <button>${{ price }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import { airlineCodes } from "../utils/airlineCodes";
import { airlineIcon, formatDateDeals } from "../utils/utils";
import Vuex from "vuex";
import { getCityThumbnail } from "../utils/cityThumbnails";

function splitLocation(location) {
  const parts = location.split(":");
  let type = "airport";
  let code;
  if (parts.length === 1) {
    code = parts[0];
  } else {
    [type, code] = parts;
  }
  return { code, type };
}

export default {
  props: ["deal"],
  delimiters: ["{{", "}}"],
  methods: {
    ...Vuex.mapMutations("search", ["setForm"]),
    ...Vuex.mapActions("search", ["search"]),
    formatDateDeals,
    getCityThumbnail,
    airlineIcon,
    searchMe() {
      this.setForm({
        place_from: {
          ...splitLocation(this.deal.fly_from),
          name: this.deal.city_from_name
        },
        place_to: {
          ...splitLocation(this.deal.fly_to),
          name: this.deal.city_to_name
        },
        adults: 1,
        children: 0,
        infants: 0,
        seat_type: "M",
        destination_type: "round",
        departure_date: this.deal.departure_date,
        return_date: this.deal.return_date
      });
      this.search({ clearFilters: true, saveSearch: true });
      this.$router.push({ name: "new-results" });
    }
  },
  computed: {
    airlines() {
      return this.deal.airlines
        .map(o => airlineCodes[o])
        .filter(o => o)
        .join(", ");
    },
    price() {
      return parseFloat(this.deal.price).toFixed(0);
    }
  }
};
</script>
