import { api } from "boot/axios";

export function reqEstrategias(context) {
  api.get("api/estrategia").then((response) => {
    context.commit("setEstrategias", response.data.results);
  });
}
