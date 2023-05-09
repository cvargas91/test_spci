import { api } from "boot/axios";
import { Cookies } from "quasar";

export function postVerificador(context, nuevoVerificador) {
  const django_token = Cookies.get("django_token");
  api
    .post("/api/verificador/", nuevoVerificador, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setNuevoVerificador", response.data);
    })
    .catch(() => {
      console.log("error verificador/postVerificador");
    });
}

export function limpiaNuevoVerificador(context) {
  context.commit("setNuevoVerificador", null);
}

export function limpiaVerificadores(context) {
  context.commit("setVerificadores", null);
}

export function reqMisVerificadores(context, id_usuario) {
  api
    .get("api/_verificador/misVerificadores")
    .then((response) => {
      context.commit("setVerificadores", response.data.datos);
    })
    .catch(() => {
      console.log("error reqMisVerificadores");
    });
}

export function reqVerificadoresUnidad(context) {
  api
    .get("api/_verificador/verificadoresUnidadSinMi/")
    .then((response) => {
      context.commit("setVerificadores", response.data.datos);
    })
    .catch(() => {
      console.log("error reqMisVerificadores");
    });
}

export function reqVerificadoresEnviadosAUPCI(context) {
  api
    .get("api/_verificador/?estado=Enviado+a+UPCI")
    .then((response) => {
      context.commit("setVerificadoresUPCI", response.data.results);
    })
    .catch(() => {
      console.log("error reqMisVerificadores");
    });
}

export async function reqVerificadorPorIndicador (context, id_indicador) {
  let indicador = id_indicador;
  api
    .get("api/_verificador/verificadorPorIndicador/?indicador=" + indicador)
    .then((response) => {
      context.commit("setVerificador", response.data.datos.verificadores);
      context.commit("setMetaVerificador", response.data.datos.total_avances.valor);
    })
    .catch(() => {
      console.log("error reqVerificadorPorIndicador");
    })
}

export function limpiaVerificadorPorIndicador (context){
  context.commit("setMetaVerificador", 0);
  context.commit("setVerificador", null);
}
