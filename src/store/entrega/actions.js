import { api } from "boot/axios";
import { Cookies } from "quasar";

export function setNuevaEntrega(context, nuevaEntrega) {
  context.commit("setNuevaEntrega", nuevaEntrega);
}

export function limpiaNuevaEntrega(context) {
  context.commit("setNuevaEntrega", null);
}

export function limpiaEntregaARechazar(context) {
  context.commit("setEntregaARechazar", null);
}

export function limpiaEntregaAFinalizar(context) {
  context.commit("setEntregaAFinalizar", null);
}

export function setAdjuntosNuevaEntrega(context, adjuntos) {
  context.commit("setAdjuntosNuevaEntrega", adjuntos);
}

export function setAdjuntosEdicionEntrega(context, adjuntosEdicionEntrega) {
  context.commit("setAdjuntosEdicionEntrega", adjuntosEdicionEntrega);
}

export function limpiaAdjuntos(context) {
  context.commit("setAdjuntosNuevaEntrega", null);
}

export function limpiaAdjuntosEdicion(context) {
  context.commit("setAdjuntosEdicionEntrega", null);
}

export async function setEntregaARechazar(context, entrega) {
  context.commit("setEntregaARechazar", entrega);
}

export async function setEntregaAFinalizar(context, entrega) {
  context.commit("setEntregaAFinalizar", entrega);
}

export async function setEntregaAModificar(context, entrega) {
  context.commit("setEntregaAModificar", entrega);
}

export function workflowEnviaAlLider(context, nuevaEntrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableEnviaALider/", nuevaEntrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "EnviadoAlLider");
    })
    .catch(() => {
      console.log("error entrega/workflowEnviaAlLider");
    });
}

export function workflowLiderDaVistoBueno(context, nuevaEntrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableLiderDaVistoBueno/", nuevaEntrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "EnviadoAUPCI");
    })
    .catch(() => {
      console.log("error entrega/workflowLiderDaVistoBueno");
    });
}

export function workflowUPCIDaVistoBueno(context, nuevaEntrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableUPCIDaVistoBueno/", nuevaEntrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "Finalizado");
    })
    .catch(() => {
      console.log("error entrega/workflowLiderDaVistoBueno");
    });
}

export function workflowLiderRechaza(context, nuevaEntrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableLiderRechaza/", nuevaEntrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
      console.log("error entrega/workflowLiderDaVistoBueno");
    });
}

export function workflowUPCIRechaza(context, nuevaEntrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableUPCIRechaza/", nuevaEntrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "RechazadoPorUPCI");
    })
    .catch(() => {
      console.log("error entrega/workflowLiderDaVistoBueno");
    });
}

export function workflowDescarta(context, entrega) {
  const django_token = Cookies.get("django_token");
  api
    .post("/entregableDescarta/", entrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      context.commit("setWorkflow", "Descartado");
    })
    .catch(() => {
      console.log("error entrega/workflowDescarta");
    });
}

export function limpiaEntregas(context) {
  context.commit("setWorkflow", null);
}

export function setRetroalimentaciones(context) {
  api
    .get("/api/retroEntrega/misRetroalimentaciones/")
    .then((response) => {
      context.commit("setRetroProductos", response.data.datos.productos);
      context.commit(
        "setRetroVerificadores",
        response.data.datos.verificadores
      );
    })
    .catch(() => {
      console.log("setRetroalimentaciones acciones");
    });
}

export function setModificaVerificador(context, entrega) {
  const django_token = Cookies.get("django_token");
  api
    //.patch("/api/editaVerificador/" + 100000 + "/", entrega, {
      .patch("/api/verificador/" + entrega.id + "/", entrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      console.log(">>>>>Verificador actualizado con exito");
    })
    .catch(() => {
      console.log("error entrega/workflowActualizaVerificador");
    });
}

export function setModificaProducto(context, entrega) {
  const django_token = Cookies.get("django_token");
  api
    //.patch("/api/editaProducto/" + id_entrega + "/", entrega, {
      .patch("/api/producto/" + entrega.id + "/", entrega, {
      headers: {
        "X-CSRFTOKEN": django_token,
      },
    })
    .then((response) => {
      console.log(">>>>>Producto actualizado con exito");
    })
    .catch(() => {
      console.log("error entrega/workflowActualizaProducto");
    });
}
