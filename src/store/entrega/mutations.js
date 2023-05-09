export function setNuevaEntrega(state, nuevaEntrega) {
  state.nuevaEntrega = nuevaEntrega;
}

export function setAdjuntosNuevaEntrega(state, adjuntos) {
  state.adjuntosNuevaEntrega = adjuntos;
}

export function setAdjuntosEdicionEntrega(state, adjuntos) {
  if (!adjuntos){
    state.adjuntosEdicionEntrega = adjuntos;
  }else{
    if(!state.adjuntosEdicionEntrega)
      state.adjuntosEdicionEntrega=[];
    var nuevoAdjunto = state.adjuntosEdicionEntrega.filter((adjuntoEdicionEntrega) => adjuntoEdicionEntrega.id !== adjuntos[0].id);

    if(nuevoAdjunto.length == state.adjuntosEdicionEntrega.length){
      state.adjuntosEdicionEntrega=state.adjuntosEdicionEntrega.concat(adjuntos);
    }else{
      state.adjuntosEdicionEntrega=nuevoAdjunto;
    }    
  }
}

export function setEntregaARechazar(state, entrega) {
  state.aRechazar = entrega;
}

export function setEntregaAFinalizar(state, entrega) {
  state.aFinalizar = entrega;
}

export function setWorkflow(state, estado) {
  state.estadoWorkflow = estado;
}

export function setRetroProductos(state, retroalimentaciones) {
  state.retroalimentacion_productos = retroalimentaciones;
}

export function setRetroVerificadores(state, retroalimentaciones) {
  state.retroalimentacion_verificadores = retroalimentaciones;
}

export function setEntregaAModificar(state, entrega) {
  state.aModificar = entrega;
}

//mover a store verificador
export function patchVerificador (state, verificadorEditado) {
  state.verificadorEditado = verificadorEditado;
}

export function patchProducto (state, productoEditado) {
  state.productoEditado = productoEditado;
}
