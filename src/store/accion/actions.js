import { api } from "boot/axios";

export function limpiaAcciones(context) {
  context.commit("setAcciones", []);
  context.commit("setTotalAcciones", 0);
}

export function limpiaFunciones(context) {
  context.commit("setFunciones", []);
}

export function limpiaHitos(context) {
  context.commit("setHitos", []);
}

export function limpiaMdvs(context) {
  context.commit("setMDVs", []);
}
export function limpiaAccionAReportar(context) {
  context.commit("setAReportar", []);
}

export function reqAcciones(context) {
  api
    .get("api/accion/")
    .then((response) => {
      context.commit("setTotalAcciones", response.data.count);
      context.commit("setAcciones", response.data.results);
    })
    .catch(() => {
      console.log("error req acciones");
    });
}

export async function reqDetalleAccion(context, id_accion) {
  await api
    .get("api/accion/" + id_accion)
    .then((response) => {
      context.commit("setTotalAcciones", 1);
      context.commit("setAcciones", response.data);
    })
    .catch(() => {
      console.log("error req acciones");
    });
}

export function reqAccionesDelUsuario(context) {
  api
    .get(
      "api/accion/?actor=" + context.rootState.usuarix.usuario.perfil.actor_id
    )
    .then((response) => {
      context.commit("setTotalAcciones", response.data.count);
      context.commit("setAcciones", response.data.results);
    })
    .catch(() => {
      console.log("error req acciones por actor");
    });
}

export function reqAccionesPorRol(context, objParams) {
  api
    .get("api/roles/rolPorRol/" + objParams.rol + "/" + objParams.origen + "/")
    .then((response) => {
      //context.commit("setTotalAcciones", response.data.length);
      context.commit("setTotalAcciones", 1);
      context.commit("setAcciones", [response.data]);
    })
    .catch(() => {
      console.log("error req acciones unidad resp. Por Rol");
    });
}

export function reqAccionesPorRolResponsable(context, id_responsable) {
  api
    .get("api/roles/rolResponsable/" + id_responsable + "/")
    .then((response) => {
      context.commit("setTotalAcciones", response.data.length);
      context.commit("setAcciones", response.data);
    })
    .catch(() => {
      console.log("error req acciones unidad resp");
    });
}

export function reqAccionesPorRolResponsablePMI (context, id_responsable) {
  api
    .get("api/roles/rolResponsablePMI/" + id_responsable + "/")
    .then((response) => {
      context.commit("setTotalAcciones", response.data.length);
      context.commit("setAcciones", response.data);
    })
    .catch(() => {
      console.log("error req acciones unidad resp");
    });
}

export function setAccionesAReportar (context, acciones) {
  context.commit("setAReportar", acciones);
}

export function reqEstrategias(context) {
  api
    .get("api/accion/estrategias/")
    .then((response) => {
      context.commit("setEstrategias", response.data);
    })
    .catch(() => {
      console.log("error req acciones otro rol");
    });
}

export function reqFuncionesPorAccion(context, id_accion) {
  api.get("api/funcion/?accion=" + id_accion).then((response) => {
    context.commit("setFunciones", response.data.results);
  });
}

export async function reqHitosPorAccion(context, id_accion) {
  let url = "api/hito/?accion=" + id_accion;
  let data = [];
  let page = 1;
  let nextPage = "&page="
  do{
      await api.get(url).then((response) => {
        data =[...data,...response.data.results];

        if(response.data.next){          
          page++;
          let indice = url.indexOf(nextPage);
          
          if(indice>=0){
            url = url.slice(0, indice) + nextPage + page;
          }else{          
            url = url + nextPage + page;
          }          
        }else{
          url = null;
        }        
      });
  }while(url != null);

  context.commit("setHitos", data);
}

export function reqMDVPorAccion(context, id_accion) {
  api.get("api/mdv/?accion=" + id_accion).then((response) => {
    context.commit("setMDVs", response.data.results);
  });
}

export function reqFiltraAcciones(context, filtros) {
  let urlParametros =
    "actor=" + filtros.actor + "&rol=" + filtros.rol + "&tipo=" + filtros.tipo + "&anio=" + filtros.anio + "&origen=" + filtros.origen;
  api.get("accionesFiltradas/?" + urlParametros).then((response) => {
    context.commit("setAcciones", response.data);
  });
}

export function reqHitosYFuncionesPorAccion(context, id_accion) {
  api.get("api/accion/hitosyfunciones/" + id_accion + "/").then((response) => {
    context.commit("setDetalleAccion", response.data);
  });
}

export function reqAniosDisponibles(context) {
  api.get("api/accion/anios_unicos/"+ 1 + "/").then((response) => {
    context.commit("setDetalleAniosAccion", response.data);
  });
}

export function origenesDisponibles(context) {
  api.get("api/accion/origen_unicos/"+ 1 + "/").then((response) => {
    context.commit("setDetalleOrigenAccion", response.data);
  });
}

export function reqMdvFuncionesEHitosPorAccion(context, id_accion) {
  api
    .get("api/accion/mdvsFuncionesEhitos/" + id_accion + "/")
    .then((response) => {
      context.commit("setDetalleAccion", response.data);
    });
}

export function reqAccionesAReporte(context, rol) {
  api
    .get("api/roles/rolResponsable/" + rol + "/")
    .then((response) => {
      context.commit("setDetalleAccionesReporte", response.data);
      context.commit("setTotalAcciones", response.data.length);
    })
    .catch(() => {
      console.log("error req acciones unidad resp");
    });
}

export function reqAccionesAReportePMI (context, rol){
  api
    .get("api/roles/rolResponsablePMI/" + rol + "/")
    .then((response) => {
      context.commit("setDetalleAccionesReporte", response.data);
      context.commit("setTotalAcciones", response.data.length);
    })
    .catch(() => {
      console.log("error req acciones unidad resp");
    });
}

export function limpiaDetalleAccion (context){
  context.commit("setDetalleAccion", null);
}

export function reqDetalleHitosAReporte(context, detalle) {
  context.commit("setDetalleHitoAReporte", detalle);
}

export async function reqDetalleIdUAysen(context, id_accion) {
  await context.commit("setDetalleIdUAysen", id_accion);
}

export function reqAccionesFiltradas(context, filtros) {
  let urlParametros =
    "actor=" + filtros.actor + "&rol=" + filtros.rol + "&tipo=" + filtros.tipo;
  api
    .get("api/accion/accionesFiltradas/?" + urlParametros + "/")
    .then((response) => {
      console.log("response nueva accion --> ", response.data);
      //context.commit("setTotalAcciones", response.data.length);
      //context.commit("setAcciones", response.data);
    })
    .catch(() => {
      console.log("error req acciones unidad resp. Por Rol");
    });
}

export function referenciaSubirEntregable(context, referencia) {
  context.commit("setReferenciaSubeEntregable", referencia);
}
