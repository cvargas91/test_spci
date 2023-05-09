export function setMisNuevasAcciones(state, misNuevasAcciones) {
  state.misNuevasAcciones = misNuevasAcciones;
}

export function setNuevaAccion(state, nuevaAccion) {
  state.nuevaAccion = nuevaAccion;
}

export function setAccionDetallada(state, accionDetallada) {
  state.editaAccion = accionDetallada;
}

export function addAccion(state, nuevaAccion) {
  if (!state.misNuevasAcciones) {
    state.misNuevasAcciones = [];
  }
  state.misNuevasAcciones.push(nuevaAccion);
}

export function quitaAccionPorId(state, id_accion) {
  state.misNuevasAcciones = state.misNuevasAcciones.filter((accion) => {
    return accion.id != id_accion;
  });
  state.editaAccion = null;
}

export function actualizacionParcialAccion(state, cambiosParciales) {
  state.editaAccion.titulo = cambiosParciales.titulo;
  state.editaAccion.objetivo = cambiosParciales.objetivo;
  state.editaAccion.proyecto = cambiosParciales.proyecto;
  state.editaAccion.modificacion = cambiosParciales.modificacion;
}
