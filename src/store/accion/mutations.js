export function setAcciones(state, acciones) {  
  state.acciones = acciones;
}

export function setDetalleAniosAccion(state, anios) {
  state.anios = anios;
}

export function setDetalleOrigenAccion(state, origenes) {
  state.origenes = origenes;
}

export function setTotalAcciones(state, totalAcciones) {
  state.totalAcciones = totalAcciones;
}
export function setEstrategias(state, estrategias) {
  state.estrategias = estrategias;
}
export function setFunciones(state, funciones) {
  state.funciones = funciones;
}
export function setHitos(state, hitos) {
  state.hitos = hitos;
}
export function setMDVs(state, MDVs) {
  state.MDVs = MDVs;
}

export function setDetalleAccion(state, detalleAccion) {
  state.detalleAccion = detalleAccion;
}

export function setAReportar(state, acciones) {
  state.aReportar = acciones;
}

export function setDetalleAccionesReporte(state, acciones) {
  state.detalleAccionesReporte = acciones;
}

export function setDetalleHitoAReporte(state, detalle) {
  const detalleMDV = detalle.detalleProductos;
  const detalleHito = detalleMDV.filter(
    (elemento) => elemento.hitos === detalle.idHito
  );

  /*const hitosPresentes = state.detalleAccion.hitos.filter(function (element){
    return detalleHito.find(valor => valor.hitos === element.value);
  });*/

  const mdvsPresentes = state.detalleAccion.mdvs.filter(function (element) {
    return detalleHito.find((valor) => valor.value === element.value);
  });

  state.mdvsAReporte = mdvsPresentes.map((elemento) => elemento.value);
  state.detalleMDVAReporte = mdvsPresentes;
}

export function setDetalleIdUAysen(state, acciones) {
  const detalleUaysen = [];

  acciones.forEach((element) => {
    detalleUaysen.push(
      state.detalleAccionesReporte.find((elemento) => elemento.id === element)
    );
  });
  state.detalleIdUaysen = detalleUaysen.map((element) => element.accion);
}

export function setReferenciaSubeEntregable(state, referencia) {
  state.referenciaSubirEntregable = referencia;
}
