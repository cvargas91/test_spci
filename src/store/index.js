import { store } from "quasar/wrappers";
import { createStore } from "vuex";
import accion from "./accion";
import usuarix from "./usuarix";
import entrega from "./entrega";
import verificador from "./verificador";
import producto from "./producto";
import poador from "./poador";
import estrategia from "./estrategia";
import actor from "./actor";
import reporte from "./reporte";

export default store(function (/* { ssrContext } */) {
  const Store = createStore({
    modules: {
      accion,
      usuarix,
      entrega,
      verificador,
      producto,
      poador,
      estrategia,
      actor,
      reporte,
    },

    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: process.env.DEBUGGING,
  });

  return Store;
});
