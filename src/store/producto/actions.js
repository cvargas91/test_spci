import { api } from "boot/axios";
import { Cookies } from "quasar";

export function postProducto(context, nuevoProducto) {
  const django_token = Cookies.get("django_token");
  api
    .post("/api/producto/", nuevoProducto, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setNuevoProducto", response.data);
    })
    .catch(() => {
      console.log("error producto/postProducto");
    });
}

export function limpiaNuevoProducto(context) {
  context.commit("setNuevoProducto", null);
}

export function limpiaProductos(context) {
  context.commit("setProductos", null);
}

export function reqMisProductos(context, id_usuario) {
  api
    .get("api/_producto/misProductos")
    .then((response) => {
      context.commit("setProductos", response.data.datos);
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqProductosUnidad(context) {
  api
    .get("api/_producto/productosUnidadSinMi/")
    .then((response) => {
      context.commit("setProductos", response.data.datos);
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqTodosProductosUnidad(context, unidad) {
  api
    .get("api/_producto/productosUnidad/" + unidad + "/")
    .then((response) => {
      context.commit("setProductos", response.data.datos);
    })
    .catch(() => {
      console.log("error reqMisProductos");
    });
}

export function reqProductosEnviadosAUPCI(context) {
  api
    .get("api/_producto/?estado=Enviado+a+UPCI")
    .then((response) => {
      context.commit("setProductosUPCI", response.data.results);
    })
    .catch(() => {
      console.log("error reqProductosEnviadosAUPCI");
    });
}

export function reqHitosReporte (context, id_accion) {
  api
    .get("api/_producto/hitosReporte/?accion=" + id_accion)
    .then((response) => {
      context.commit("setTotalHitosReporte", response.data.mdv);
    })
    .catch(() => {
      console.log("error hitosReporte");
    });
}

