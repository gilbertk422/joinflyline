<template>
  <div class="booking-view row">
    <div class="col-8 offset-2">
      <div class="row description-block">
        <div class="col-12">
          <div class="booking-box">
            <h2>Your trip is booked!</h2>
            <p>
              It looks like you found a great deal! Pack your bags cause you
              have a trip coming up. You’re probably wondering what’s next, not
              to worry, we have the answers for you!
            </p>
            <p>
              After booking your flight, you will receive an email from FlyLine
              (us), notifying you that we have received your booking. Next, you
              will receive either an additional email from us or one of our
              ticketing partners. Leading up to your trip, you will continue to
              receive emails regarding your trip, so be sure to keep an eye on
              your inbox. If you have any questions, feel free to contact us.
            </p>
          </div>
        </div>
      </div>
      <div class="row summary-block">
        <div class="col-8">
          <div class="booking-box trip-summary">
            <div class="box-header">
              <h2>Trip Summary</h2>
              <span>4 Nights Stay in Chicago</span>
            </div>
            <div class="box-body row">
              <div class="col-6 trip-section">
                <h4>Depature</h4>
                <div class="economy-section">
                  <span class="date">20 March</span>
                  <a class="economy">Economy</a>
                </div>
                <div class="detail">
                  <div class="time-table">
                    <div class="time-pick">
                      <b>06:10 AM</b>
                      New York LGA
                    </div>
                    <div class="time-pick">
                      <b>07:47 AM</b>
                      Chicago ORD
                    </div>
                  </div>
                  <img src="@/assets/images/dashboard/mark-3.png" />
                </div>
                <div class="duration">
                  2h 37m
                </div>
              </div>
              <div class="col-6 trip-section">
                <h4>Return</h4>
                <div class="economy-section">
                  <span class="date">24 March</span>
                  <a class="economy">Economy</a>
                </div>
                <div class="detail">
                  <div class="time-table">
                    <div class="time-pick">
                      <b>06:10 AM</b>
                      New York LGA
                    </div>
                    <div class="time-pick">
                      <b>07:47 AM</b>
                      Chicago ORD
                    </div>
                  </div>
                  <img src="@/assets/images/dashboard/mark-3.png" />
                </div>
                <div class="duration">
                  2h 37m
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="booking-box trip-cost">
            <h4>Trip Cost</h4>
            <div class="cost-item">
              <span class="item-name">1 Passenger</span>
              <span class="item-price">$165.00</span>
            </div>
            <div class="cost-item">
              <span class="item-name">Baggage</span>
              <span class="item-price">$0.00</span>
            </div>
            <div class="cost-item">
              <span class="item-name">Automatic flight check-in</span>
              <span class="item-price">Free</span>
            </div>
            <hr />
            <div class="total-item">
              <span class="total">Trip Total</span>
              <span class="total-price">$165.00</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardUIBooking"
};
</script>

<style lang="scss">
.booking-view {
  font-family: Dona-regular;
  padding-top: 5rem;
  .booking-box {
    background: #ffffff;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
    width: 100%;
  }

  .description-block {
    margin-bottom: 1.25rem;
    h2 {
      font-family: dona-bold;
      font-size: 1.4rem;
      line-height: 1.5rem;
      color: #000000;
      margin-bottom: 0.375rem;
    }

    p {
      font-family: dona-regular;
      font-size: 0.75rem;
      line-height: 1.25rem;
      color: #000000;
      margin-bottom: 1rem;
    }

    .booking-box {
      padding: 1.25rem 5rem 0.25rem 1.75rem;
    }
  }

  .summary-block {
    .trip-summary {
      padding: 1.25rem;
      padding-bottom: 2rem;

      .box-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.25rem;
        h2 {
          font-family: dona-bold;
          font-size: 1.4rem;
          line-height: 1.5rem;
          color: #000000;
          margin-bottom: 0;
          margin-right: 1rem;
        }

        span {
          font-family: dona-regular;
          font-size: 0.625rem;
          line-height: 0.75rem;
          color: #000000;
        }
      }

      .box-body {
        .trip-section {
          h4 {
            font-family: dona-bold;
            font-size: 1rem;
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
                font-size: 0.75rem;
                line-height: 0.75rem;
                color: #000000;
                margin-bottom: 0.4rem;

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
    }

    .trip-cost {
      padding: 1.25rem 0.75rem;

      h4 {
        font-family: dona-bold;
        font-size: 1.4rem;
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
          font-size: 0.65rem;
          line-height: 0.75rem;
          color: #000000;
        }

        .item-price {
          font-weight: bold;
          font-size: 0.75rem;
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
          font-family: dona-bold;
          font-size: 1.4rem;
          line-height: 1.125rem;
          color: #000000;
        }

        .total-price {
          font-family: dona-bold;
          font-size: 1.2rem;
          line-height: 1.125rem;
          text-align: right;
          color: #000000;
        }
      }
    }
  }
}
</style>
