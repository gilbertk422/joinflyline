<template>
  <div class="fare-view row booking-page">
    <div class="col-8 offset-2">
      <div class="row summary-block summary-right">
        <trip-summary />

        <div class="booking-box trip-summary">
          <div class="box-header">
            <h2>Where to Book</h2>
          </div>
          <div class="box-subheader">
            Click the ‘book’ button, you’ll be routed to the site to book the
            meta fare
          </div>
          <div class="box-body">
            <div class="meta-fare__where-content">
              <div>
                <img :src="providerIcon(flightToBook.provider)" alt="" />
                Route to {{ flightToBook.provider }} site to view this meta fare
              </div>
              <div class="btn box-btn">
                <a :href="flightToBook.deeplink"
                  >Cheapest Fare ${{ flightToBook.price }}</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TripSummary from "../TripSummary";
import Vuex from "vuex";
import { providerIcon } from "../../utils/utils";

export default {
  name: "DashboardUIFare",
  components: {
    TripSummary
  },
  data() {
    return {
      items: [
        {
          active: false,
          title: "What is a Meta Fare",
          content: `Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Mollitia fugiat perferendis, quam quos nemo debitis. Nesciunt
                dolores ipsa eum veritatis voluptatibus, eligendi deserunt,
                quasi assumenda, sequi quisquam quibusdam harum repudiandae.`
        },
        {
          active: false,
          title: "How to book a Meta Fare",
          content: `Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Molestias numquam aut non reprehenderit quae, amet
                necessitatibus minus, blanditiis odit, hic officia cum dolorum
                expedita veniam. Nemo quae repellendus perferendis in!`
        },
        {
          active: false,
          title: "Can I earn a frequent flyer miles on Meta Fares",
          content: `Lorem ipsum dolor sit, amet consectetur adipisicing elit.
                Ducimus, illum earum tempore commodi cumque fuga ad obcaecati
                aliquid officia ratione, optio ab voluptas repudiandae iure.
                Error quam quaerat distinctio ex.`
        }
      ]
    };
  },
  methods: {
    handleClick(index) {
      this.items[index].active = !this.items[index].active;
    },
    providerIcon
  },
  computed: {
    ...Vuex.mapGetters("search", ["flightToBook"])
  }
};
</script>

<style lang="scss">
@import "src/assets/styles/general/variables";
@import "src/assets/styles/mixins/mq";
@import "src/assets/styles/components/booking";

.fare-view {
  padding-top: 5rem;
  .booking-box {
    background: #ffffff;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
    width: 100%;
    margin-bottom: 10px;
  }

  .summary-block {
    .trip-summary {
      padding: 1.25rem;
      padding-bottom: 2rem;

      .box-header {
        display: flex;
        align-items: baseline;
        margin-bottom: 1.25rem;

        h2 {
          font-weight: 900;
          font-size: 1.125rem;
          line-height: 1.5rem;
          color: #000000;
          margin-bottom: 0;
          margin-right: 1rem;
        }

        span {
          font-weight: bold;
          font-size: 0.625rem;
          line-height: 0.75rem;
          color: #000000;
        }
      }

      .box-body {
        .trip-section {
          h4 {
            font-size: 1.125rem;
            line-height: 1rem;
            color: #000000;
            margin-bottom: 1rem;
          }

          .economy-section {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.25rem;
            .date {
              font-weight: bold;
              font-size: 0.625rem;
              line-height: 0.75rem;
              color: #000000;
            }

            .economy {
              font-weight: bold;
              font-size: 0.5rem;
              line-height: 0.625rem;
              color: #00aeef;
            }
          }

          .detail {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.625rem;
            padding-bottom: 0.375rem;
            border: 1px solid #d4d4d4;
            margin-bottom: 0.5rem;

            .time-table {
              .time-pick {
                font-size: 0.625rem;
                line-height: 0.75rem;
                color: #000000;
                margin-bottom: 0.125rem;

                b {
                  font-weight: bold;
                }
              }
            }

            img {
              width: 1.75rem;
              height: 1.75rem;
            }
          }

          .duration {
            width: 100%;
            font-weight: bold;
            font-size: 0.5rem;
            line-height: 0.625rem;
            text-align: right;
            color: #000000;
          }
        }
      }

      .box-btn {
        border: 1px solid #00aeef;
        font-weight: 900;
        font-size: 10px;
        color: #000000;
        text-align: center;
        padding-left: 2rem;
        padding-right: 2rem;
      }
    }

    .trip-cost {
      padding: 1.25rem 0.75rem;

      h4 {
        font-weight: bold;
        font-size: 1.25rem;
        line-height: 1.5rem;
        color: #000000;
        margin-bottom: 1.25rem;
      }

      .cost-item {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        margin-bottom: 0.75rem;
        .item-name {
          font-weight: bold;
          font-size: 0.625rem;
          line-height: 0.75rem;
          color: #000000;
        }

        .item-price {
          font-weight: bold;
          font-size: 0.875rem;
          line-height: 1rem;
          text-align: right;
          color: #000000;
        }
      }

      hr {
        margin-top: 0.5rem;
        margin-bottom: 1.25rem;
        border-top: 1px solid #d8d8d8;
      }

      .total-item {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        .total {
          font-weight: bold;
          font-size: 1rem;
          line-height: 1.125rem;
          color: #000000;
        }

        .total-price {
          font-weight: bold;
          font-size: 1rem;
          line-height: 1.125rem;
          text-align: right;
          color: #000000;
        }
      }
    }
  }

  .box-subheader {
    font-weight: bold;
    font-size: 8px;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px #d8d8d8 solid;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
  }
}

.meta-fare__where-content {
  font-weight: bold;
  font-size: 10px;
  color: #000000;
  display: flex;
  justify-content: space-between;

  img {
    width: 48px;
  }
}

.meta-fare__list {
}

.meta-fare__list-item {
  padding-top: 1px;
  &.is-active {
    margin-bottom: 1rem;
  }
}

.meta-fare__list-head {
  font-weight: 900;
  font-size: 12px;
  color: #000000;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;

  &:after {
    content: "";
    background-image: url("data:image/svg+xml,%3Csvg width='17' height='9' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0l8.5 8L17 0v1L8.5 9 0 1z' fill='%23BBB' fill-rule='evenodd'/%3E%3C/svg%3E");
    width: 17px;
    height: 9px;
    transition: transform 0.25s ease;
  }

  .meta-fare__list-item.is-active &:after {
    transform: rotate(180deg);
  }
}

.meta-fare__list-body {
}
</style>
