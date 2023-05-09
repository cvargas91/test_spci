import { boot } from "quasar/wrappers";

export default async ({ app, router, store }) => {
  await store.dispatch("usuarix/reqDatosIniciales");
};
