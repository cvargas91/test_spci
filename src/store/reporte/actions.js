import { api } from "boot/axios";
import { Cookies } from "quasar";

export function postReporte (context, nuevoReporte) {
    const django_token = Cookies.get("django_token");
    api.
        post("/api/reporte/", nuevoReporte, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {
            console.log(">>>>>reporte Almacenado con exito");
        })
        .catch(() => {
            console.log(">>>>>error reporte/postReporte");
        });
}

export function patchReporte (context, nuevoReporte) {
    const django_token = Cookies.get("django_token");
    api.
        //patch("/api/reporte/editaReporte/", nuevoReporte, {
            patch("/api/reporte/"+ nuevoReporte.id + "/", nuevoReporte, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {            
            if (response.data.tipo === "POA"){
                context.commit("setActualizarReporteFinalizados", response.data);
            }else{
                context.commit("setActualizarReporteFinalizadosPMI", response.data);
            }
            
            console.log(">>>>>reporte Actualizado con exito");
        })
        .catch(() => {
            console.log(">>>>>error reporte/patchstReporte");
        });
}

export function setNuevoReporte(context, nuevoReporte) {
    context.commit("setNuevoReporte", nuevoReporte);
};

export function actalizaNuevoReporte (context, nuevoReporte) {
    context.commit("setCambioNuevoReporte", nuevoReporte);
}

export function setNuevoReporteFuncion (context, nuevoReporteFuncion){
    context.commit("setNuevoReporteFunciones", nuevoReporteFuncion);
}

export function setNuevoReporteHito (context, nuevoReporteHito){
    context.commit("setNuevoReporteHitos", nuevoReporteHito);
}

export function actualizaNuevoReporteAccion (context, reporteAccion){
    context.commit("setCambioNuevoReporteAccion", reporteAccion);
}

export function actualizaNuevoReporteHito (context, reporteHito) {
    context.commit("setCambioNuevoReporteHitos", reporteHito);
}

export function actualizaNuevoReporteFuncion (context, reporteFuncion) {
    context.commit("setCambioNuevoReporteFunciones", reporteFuncion);
}

export function actualizaNuevoReporteFuncionPMI (context, funcion) {
    context.commit("setCambioNuevoReporteFuncionesPMI", funcion);
}

export function actualizaReporteFuncionPMI (context, funcion) {
    context.commit("setCambioReporteFuncionesPMI", funcion);
}

export function limpiaNuevoReporte(context){
    context.commit("setNuevoReporte", null);
}

export function setReporteAcciones(context, reporteAccion){

    context.commit("setReporteAcciones", reporteAccion);
}

//Se toman funciones, hitos y mdv de manera independiente para generar reporte
export function setFuncionesPorAccionParaReporte(context, reporteFunciones) {
    context.commit("setReporteFunciones", reporteFunciones);
}

export function setHitosPorAccionParaReporte(context, repoteHitos) {
    context.commit("setReporteHitos", repoteHitos);
}

export function setMDVPorAccionParaReporte(context, reporteMDVs) {
    context.commit("setReporteMDVs", reporteMDVs);
}

export function limpiaReporteFunciones(context) {
    context.commit("setReporteFunciones", null);
}

export function limpiaReporteHitos(context) {
    context.commit("setReporteHitos", null);
}


export function limpiaReporteAccion(context){
    context.commit("setReporteAcciones", null);
}

export function reqReportesUpci(context){
    api.
        get("api/reporte/reportesUpci")
        .then((response) => {
            context.commit("setReporteFinalizado", response.data.datos.finalizados);
            context.commit("setReporteFinalizadoPMI", response.data.datos.finalizadosPMI);
        }).catch(() => {
            console.log("error reqReportesUpci");
        });
}

export function reqReportesBorradores(context) {
    api
        .get("api/reporte/misReportes")
        .then((response) => {
            context.commit("setReporteBorrador", response.data.datos.borradores);
            context.commit("setReporteBorradorPMI", response.data.datos.borradoresPMI);
        })
        .catch(() => {
            console.log("error reqReportesBorradores");
        });
}


export function setReporteAEditar (context, reporte) {
    context.commit("setReporteAEditar", reporte);
}

export function setReporteAccionesAEditar (context, reporteAccion){
    context.commit("setReporteAccionesAEditar", reporteAccion);
}

export function setReporteHitosAEditar (context, reporteHito) {
    context.commit("setReporteHitosAEditar", reporteHito);
}

export function setReporteFuncionesAEditar (context, reporteFuncion) {
    context.commit("setReporteFuncionesAEditar", reporteFuncion);
}

export function actualizaReporteFunciones (context, reporteFuncion) {
    context.commit("setCambioReporteFuncionesAEditar", reporteFuncion);
}

export function actualizaReporteHitos (context, reporteHito) {
    context.commit("setCambioReporteHitosAEditar", reporteHito);
}

export function actualizaReporteAcciones (context, reporteAccion) {
    context.commit("setCambioReporteAccionesAEditar", reporteAccion);
}

export function limpiaReporteAEditar (context) {
    context.commit("setReporteAEditar", null);
}

export function limpiaReporteFuncionesAEditar (context){
    context.commit("setReporteFuncionesAEditar", null);
}

export function limpiaReporteHitosAEditar (context){
    context.commit("setReporteHitosAEditar", null);
}

export async function generaReporte(context, arregloReporteUnidad) {
    let id_reporte = arregloReporteUnidad[2];
    const django_token = Cookies.get("django_token");
    await api
        .get("/generarPdf/"+ id_reporte, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
            responseType: 'blob',
        })
        .then((response) => {
            //window.open(URL.createObjectURL(response.data));
            const anchor = document.createElement('a')
            anchor.href = window.URL.createObjectURL(response.data)
            anchor.download = 'Reporte_' + arregloReporteUnidad[0] + "_" + arregloReporteUnidad[1]
            anchor.click()
            URL.revokeObjectURL(anchor.href);
        })
        .catch(() => {
            console.log("error reporte/generarPdf");
        });
}

export async function generaReportePMI(context, arregloReporteUnidad) {
    let id_reporte = arregloReporteUnidad[2];
    const django_token = Cookies.get("django_token");
    await api
        .get("/generarPdfPMI/"+ id_reporte, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
            responseType: 'blob',
        })
        .then((response) => {
            //window.open(URL.createObjectURL(response.data));
            const anchor = document.createElement('a')
            anchor.href = window.URL.createObjectURL(response.data)
            anchor.download = 'Reporte_PMI_' + arregloReporteUnidad[0] + "_" + arregloReporteUnidad[1]
            anchor.click()
            URL.revokeObjectURL(anchor.href);
        })
        .catch(() => {
            console.log("error reporte/generarPdfPMI");
        });
}


/* REPORTE NAV. POA */
export async function generaReporteNavegadorPOA(context, contenidoSeparado ) {
    var encodedUri = encodeURI(contenidoSeparado);
    var link = document.createElement("a");
    link.setAttribute("href", "data:text/csv;charset=utf-8,%EF%BB%BF" +  escape(contenidoSeparado));
    
    link.setAttribute("download", "datos_del_navegador_poa.csv");
    link.click(); 
}
/* REPORTE NAV. POA */


export async function reqTotalMetasPorFuncion (context, id_funcion) {
    api
    .get("api/indicador/metaPorFuncion/?funcion=" + id_funcion)
    .then((response) => {
        context.commit("setMeta", response.data.datos.total_meta_funcion.valor);
    })
    .catch(() => {
        console.log("error reqVerificadorPorIndicador");
    })
}

