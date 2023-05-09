export function setNuevoReporte(state, nuevoReporte){
    
    nuevoReporte.acciones.forEach(element => {  
        
        const reporteAccion = {
            "accion" : element.accion.id,
            "estado_ejecucion": "",
            "justificacion_contingencia": "",
            "reporte_justificacion_contingencia": "",
            "reporte_funciones" : [],
            "reporte_hitos": []
        };    

        nuevoReporte.reporte.reporte_acciones.push(reporteAccion);
    });


    state.nuevoReporte = nuevoReporte.reporte;
};

export function setCambioNuevoReporte (state, nuevoReporte){    
    state.nuevoReporte = nuevoReporte;
};

export function setCambioNuevoReporteAccion (state, reporteAccion) {
    const indiceAReemplazar = state.nuevoReporte.reporte_acciones.findIndex(elemento => elemento.accion === reporteAccion.accion);
    state.nuevoReporte.reporte_acciones[indiceAReemplazar] = reporteAccion;
};

export function setNuevoReporteFunciones (state, nuevoReporteFuncion) {
    state.nuevoReporteFunciones = nuevoReporteFuncion;
};

export function setCambioNuevoReporteFuncionesPMI (state, funcion) {
    const nuevoReporteFuncion = {
        id_tactica : "F01",
        funcion : funcion,
        indicador : "0",
        comentario_cumplimiento : "0"
    };
    setCambioNuevoReporteFunciones(state, nuevoReporteFuncion);
}

export function setCambioReporteFuncionesPMI (state, funcion) {
    const reporteFuncion = {
        id_tactica : "F01",
        funcion : funcion,
        indicador : "0",
        comentario_cumplimiento : "0"
    };
    setCambioReporteFuncionesAEditar(state, reporteFuncion);
}

export function setActualizarReporteFinalizados(state, reporteActualizado) {
    const indiceAReemplazar = state.finalizado.findIndex(elemento => elemento.id === reporteActualizado.id);    
    state.finalizado[indiceAReemplazar] = reporteActualizado;    
};

export function setActualizarReporteFinalizadosPMI(state, reporteActualizado) {
    const indiceAReemplazar = state.finalizadoPMI.findIndex(elemento => elemento.id === reporteActualizado.id);
    state.finalizadoPMI[indiceAReemplazar] = reporteActualizado;    
};

export function setCambioNuevoReporteFunciones (state, reporteFuncion) {
    
    if (state.nuevoReporteFunciones.length){
    
        const indiceAReemplazar = state.nuevoReporteFunciones.findIndex(elemento => elemento.funcion === reporteFuncion.funcion);
        if(indiceAReemplazar >= 0) {
            state.nuevoReporteFunciones[indiceAReemplazar] = reporteFuncion;
        }else{
            state.nuevoReporteFunciones.push(reporteFuncion);    
        }
    }else{
        state.nuevoReporteFunciones.push(reporteFuncion);
    } 
};

export function setNuevoReporteHitos (state, nuevoReporteHito) {
    state.nuevoReporteHitos = nuevoReporteHito;
}

export function setCambioNuevoReporteHitos (state, reporteHito) {
    if(state.nuevoReporteHitos.length){
        const indiceAReemplazar = state.nuevoReporteHitos.findIndex(elemento => elemento.hito === reporteHito.hito);
        if(indiceAReemplazar >= 0) {
            state.nuevoReporteHitos[indiceAReemplazar] = reporteHito;
        }else{
            state.nuevoReporteHitos.push(reporteHito);    
        }
    }else{
        state.nuevoReporteHitos.push(reporteHito);
    }
}

export function setReporte (state, reporte){
    state.reporte = reporte;
}
export function setNuevoReporteBorrador(state, reporte){
    state.borrador = reporte;
}
export function setReporteBorrador (state, reporte){
    state.borrador = reporte;
}

export function setReporteBorradorPMI (state, reporte){
    state.borradorPMI = reporte;
}

export function setReporteFinalizado (state, reporte){
    state.finalizado = reporte;
}

export function setReporteFinalizadoPMI (state, reporte){
    state.finalizadoPMI = reporte;
}

export function setReporteAcciones(state, reporteAccion) {
    if(!state.reporteAcciones){
        if(reporteAccion){
            state.reporteAcciones = [reporteAccion];
        }
    }else{
        if(reporteAccion){
            state.reporteAcciones.push(reporteAccion);
        }else{
            state.reporteAcciones = reporteAccion;
        }
    }
}

export function setReporteFunciones(state, reporteFunciones) {    
    if(!state.reporteFunciones){
        if(reporteFunciones){
            state.reporteFunciones = [reporteFunciones];
        }
    }else{
        if(reporteFunciones){
            state.reporteFunciones.push(reporteFunciones);
        }else{
            state.reporteFunciones = reporteFunciones
        }
    }
}

export function setReporteHitos(state, reporteHitos) {
    if(!state.reporteHitos){
        if(reporteHitos){
            state.reporteHitos = [reporteHitos];
        }
    }else {
        if(reporteHitos){
            state.reporteHitos.push(reporteHitos);
        }else{
            state.reporteHitos = reporteHitos;
        }
    }
}

export function setReporteAEditar (state, reporte) {
    state.aEditar = reporte;
}

export function setMeta(state, metaTotal) {
    state.total_meta = metaTotal;
}

export function setReporteAccionesAEditar (state, reporteAccion){
    state.reporteAccionesAEditar = reporteAccion;
}

export function setReporteHitosAEditar (state, reporteHito){
    state.reporteHitosAEditar = reporteHito;
}

export function setReporteFuncionesAEditar (state, reporteFuncion){
    state.reporteFuncionesAEditar = reporteFuncion;
}

export function setCambioReporteFuncionesAEditar (state, reporteFuncion){

    if (state.reporteFuncionesAEditar.length){
        const indiceAReemplazar = state.reporteFuncionesAEditar.findIndex(elemento => elemento.funcion === reporteFuncion.funcion);
        if(indiceAReemplazar >= 0) {
            state.reporteFuncionesAEditar[indiceAReemplazar] = reporteFuncion;
        }else{
            state.reporteFuncionesAEditar.push(reporteFuncion);    
        }
    }else{
        state.reporteFuncionesAEditar.push(reporteFuncion);
    } 
}

export function setCambioReporteHitosAEditar (state, reporteHito){   

    if(state.reporteHitosAEditar.length){
        
        const indiceAReemplazar = state.reporteHitosAEditar.findIndex(elemento => elemento.hito === reporteHito.hito);
        if(indiceAReemplazar >= 0) {
            
            state.reporteHitosAEditar[indiceAReemplazar] = reporteHito;
        }else{
            state.reporteHitosAEditar.push(reporteHito);    
        }
    }else{
        state.reporteHitosAEditar.push(reporteHito);
    }
    
}

export function setCambioReporteAccionesAEditar (state, reporteAccion){
    const indiceAReemplazar = state.aEditar.reporte_acciones.findIndex(elemento => elemento.accion === reporteAccion.accion);
    state.aEditar.reporte_acciones[indiceAReemplazar] = reporteAccion;
}
