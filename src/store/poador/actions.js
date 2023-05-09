import { api } from "boot/axios";
import { Cookies } from "quasar";

export function reqMisNuevasAcciones(context, id_usuario) {
  api
    .get("api/protoAccion/")
    .then((response) => {
      context.commit("setMisNuevasAcciones", response.data.results);
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqDetalleAccion(context, id_accion) {
  api
    .get("api/_protoAccion/" + id_accion)
    .then((response) => {
      context.commit("setAccionDetallada", response.data);
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqNuevaAccion(context, nuevaAccion) {
  const django_token = Cookies.get("django_token");
  api
    .post("api/protoAccion/", nuevaAccion, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("addAccion", response.data);
      context.commit("setNuevaAccion", response.data);
    })
    .catch((e) => {
      console.log("error reqNuevaAccion: " + e.message);
    });
}

export function cancelaEdicion(context) {
  context.commit("setAccionDetallada", null);
}

export function reqEliminaAccion(context, id_accion) {
  api
    .delete("api/_protoAccion/" + id_accion)
    .then((response) => {
      if (response.status == 204) {
        context.commit("quitaAccionPorId", id_accion);
      }
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqActualizaAccion(context, nuevaAccionParcial) {
  api
    .patch("api/protoAccion/" + nuevaAccionParcial.id + "/", nuevaAccionParcial)
    .then((response) => {
      context.commit("actualizacionParcialAccion", response.data);
    })
    .catch((e) => {
      console.log("error reqNuevaAccion: " + e.message);
    });
}

export function agregaEstrategia(context, id_accion_estrategia) {
  api
    .patch("api/_protoAccion/agregaEstrategia/", id_accion_estrategia)
    .then((response) => {
      context.commit("setAccionDetallada", response.data);
    })
    .catch((e) => {
      console.log("error agregaEstrategia: " + e.message);
    });
}

export function quitaEstrategia(context, id_accion_estrategia) {
  api
    .patch("api/_protoAccion/quitaEstrategia/", id_accion_estrategia)
    .then((response) => {
      context.commit("setAccionDetallada", response.data);
    })
    .catch((e) => {
      console.log("error quitaEstrategia: " + e.message);
    });
}
