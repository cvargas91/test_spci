import { api } from "boot/axios";

export async function reqDatosIniciales(context) {
  let response = await api.get("datosIniciales/");
  context.commit("setUsuario", response.data.usuario);
  context.commit("setOpciones", response.data.opciones);
}

export async function reqAccessToken(context) {
  let response = await api.get("getCredentials/");
  context.commit("setAccessToken", response.data.g_access_token);
}
