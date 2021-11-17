import api from "../utils/http";

export const userStorage = {
  keys: {
    token: "authToken",
    tokenExpiry: "authTokenExpiry"
  },

  /**
   * Stores user sesstion to localstorage
   * @param {string} token
   * @param {string} expiry
   */
  setSession(token, expiry) {
    localStorage.setItem(this.keys.token, token);
    localStorage.setItem(this.keys.tokenExpiry, expiry);
  },

  dropSession() {
    localStorage.removeItem(this.keys.token);
    localStorage.removeItem(this.keys.tokenExpiry);
  },
  /**
   * @returns {{string|null)}
   */
  get token() {
    if (this.isExpired) {
      this.dropSession();
    }
    return localStorage.getItem(this.keys.token);
  },

  /**
   * @returns {string}
   */
  get tokenExpiry() {
    return localStorage.getItem(this.keys.tokenExpiry);
  },

  /**
   * @returns {boolean}
   */
  get isExpired() {
    return new Date() > new Date(this.tokenExpiry);
  },

  /**
   * @returns {boolean}
   */
  get isSessionValid() {
    return !(this.isExpired || this.token === null);
  }
};

export const userStore = {
  namespaced: true,
  state: {
    authErrorText: "",
    user: { anonymous: true }
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuthError(state, value) {
      state.authErrorText = value;
    },
    CLEAR_STATUS(state) {
      state.authErrorText = "";
    }
  },
  actions: {
    clearStatus(context) {
      context.commit("CLEAR_STATUS");
    },
    initializeUser(context) {
      if (localStorage.getItem("authToken") === null) {
        return;
      }
      return api
        .get("/users/me/")
        .then(response => {
          const user = Object.assign({}, { anonymous: false }, response.data);
          context.commit("setUser", user);
          context.dispatch("deals/fetchUserDeals", user, { root: true });
          context.dispatch("deals/fetchRandomDeals", user, { root: true });
          context.dispatch("deals/fetchFeedDeals", user, { root: true });
        })
        .catch(err => {
          if (err.response.status === 401) {
            userStorage.dropSession();
            context.commit("setUser", { anonymous: true });
            context.dispatch("deals/reset", null, { root: true });
          }
        });
    },
    logOut(context, router) {
      api.post("/auth/logout/").then(() => {
        localStorage.removeItem("authToken");
        context.commit("setUser", { anonymous: true });
        window.Intercom("shutdown");
        router.push(
          {
            name: "index"
          },
          () => {
            window.Intercom("boot", {
              app_id: "mkmh7651"
            });
          }
        );
      });
    },
    authenticate(ctx, params) {
      const { email, password, router, name } = params;
      api
        .post(
          "/auth/login/",
          {},
          {
            headers: {
              Authorization: "Basic " + btoa(`${email}:${password}`)
            }
          }
        )
        .then(response => {
          if (response.status < 400) {
            userStorage.setSession(response.data.token, response.data.expiry);
            ctx.dispatch("initializeUser").then(() => {
              window.Intercom("shutdown");
              router.push(
                {
                  name
                },
                () => {
                  window.Intercom("boot", {
                    app_id: "mkmh7651",
                    email
                  });
                }
              );
            });
          }
        })
        .catch(error => {
          if (error.response.status === 401) {
            ctx.commit("setAuthError", "Incorrect Email or Password");
          } else {
            ctx.commit("setAuthError", "Something went wrong");
          }
        });
    }
  },
  getters: {
    user(state) {
      return state.user;
    }
  }
};
