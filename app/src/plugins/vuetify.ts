/*
 * Dog Bark Detection App
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        options: {
            customProperties: true,
        },
        themes: {
            light: {
                primary: "#8e24aa",
                secondary: "#424242",
                accent: "#82b1ff",
                error: "#ff5252",
                info: "#2196f3",
                success: "#4caf50",
                warning: "#ffc107",
            },
        },
    },
});
