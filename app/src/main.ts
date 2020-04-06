/*
 * Dog Bark Detection App
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import App from "@/App.vue";

import "@/registerServiceWorker";

import router from "@/router";
import store from "@/store";
import vuetify from "@/plugins/vuetify";

Vue.config.productionTip = false;

// noinspection JSUnusedGlobalSymbols
new Vue({
    router,
    store,
    vuetify,
    render: h => h(App),
}).$mount("#app");
