<style scoped>
    #logo {
        width: 6em;
        height: auto;
        padding: 0.2em;
    }
</style>
<template>
    <q-card 
        class="my-card" 
        align="center"
        flat bordered
    >
        <div title="header">
            <p align="center" style="margin-bottom: 1,0cm; line-height: 30%">
            <img 
                id="logo"
                src="/static/uaysen-nuevo-1.png"
                name="image1.jpg" 
                align="bottom" 
                width="70" 
                height="90" 
                border="0"/>
            </p>
        </div>
        
        <div>
            <p align="center" style="margin-bottom: 0.2cm; line-height: 40%; font-size=20pt">
                <b>REPORTE MEDIOS DE VERIFICACIÓN</b>
            </p>
        </div>
        <div>
            <p align="center" style="margin-bottom: 0.2cm; line-height: 108%">
                <b>Planificación Operativa Anual {{ anio }}</b>
            </p>
        </div>
        <div>
            <p align="center" style="margin-bottom: 0cm; line-height: 90%; page-break-before: auto;">
                <b>{{mes}}</b>
            </p>
        </div>
        <br/>
        
        <br/>
        
        <q-card-section 
            transition-prev="slide-down"
            transition-next="slide-up"
            v-if="!finReporteAccion"
        >
        <div align="center">
            
            <q-card 
                style="width:65%"
                flat bordered
            >   
                <q-card-section horizontal style="height:auto">
                    <q-item-label class="col-2 bg-blue-2" flat bordered>
                        <b style="font-size: 11pt;text-align: center">Título Acción</b>
                    </q-item-label>
                    <q-separator vertical />
                        <q-item-label class="col bg-deep-orange-1" flat bordered >
                            <b>{{accionesAReportar.titulo}}</b>
                        </q-item-label>
                </q-card-section>
                <q-separator horizontal />
                <q-card-section horizontal style="height: 55px">
                    <q-item-label class="col bg-blue-2" style="padding-top: 8px;">
                        <b style="text-align: center;">Identificador Acción</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col-4">
                        
                        <q-select
                            v-model="model"
                            :options="opciones"
                            :option-label="(item) => item === null ? 'Null' : getAccion(item.accion)"
                            @update:model-value="cambio"
                        />
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col-4 bg-blue-2" style="padding-top: 8px;">
                        <b>Unidad Responsable</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col" style="padding-top: 8px;">
                        <b>{{defineActor(accionesAReportar.rol_set)}}</b>
                    </q-item-label>
                </q-card-section>
                <q-separator horizontal />
                <q-card-section horizontal style="height:auto;">
                    <q-item-label class="col-2 bg-blue-2" flat bordered style="padding-top: 5px;" >
                        <b style="font-size: 11pt;text-align: center">Tributa Proceso de Acreditación:</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col bg-deep-orange-1" flat bordered style="padding-top: 5px; padding-bottom: 5px;" v-if="accionesAReportar.origen == 'PMI'">
                        Proceso de Acreditación.                        
                    </q-item-label>
                    <q-item-label class="col bg-deep-orange-1" flat bordered style="padding-top: 5px; padding-bottom: 5px;" v-else-if="accionesAReportar.estrategias.length > 1">
                        Proceso de Acreditación.
                    </q-item-label>
                    <q-item-label class="col bg-deep-orange-1" flat bordered style="padding-top: 5px; padding-bottom: 5px;" v-else>
                        No tributa.                    
                    </q-item-label>
                </q-card-section>
            </q-card>
            <q-space />
            <br/>
            <q-space />
            <br/>
            <br/>
            <div v-if="cambia">
            <div align="center" v-if="acciones.funciones.length">
                <ReporteFuncionesEdicion
                    :reporteAccion="model"
                    :reporteFunciones="model.reporte_funciones"
                    :identificador="accionesAReportar.id_uaysen"
                />
            </div>

            <div align="center" v-if="validaReporteHito()">    
                <ReporteHitosEdicion
                    :reporteAccion="model"
                    :identificador="accionesAReportar.id_uaysen"
                />
            </div>

            <div align="center" v-if="validaReporteAccion()">
                <ReporteAccionesEdicion
                    :fechaFormateada="fechaFormateada"
                    :opcionesJustificacion="opcionesJustificacion"
                    :reporteAccion="model"
                    @cambioReporteAccion="cambioReporteAccion"
                    @finReporte="finReporte"
                />
            </div>

            </div>
            <q-space />
            <br/>
        </div>
        </q-card-section> 
                
        <q-card-section
            transition-prev="slide-down"
            transition-next="slide-up"
            v-if="finReporteAccion"
        >
            <div align="center" style="height: auto; ">
                <q-card
                    style="width:65%"
                    flat bordered
                >
                    <q-card-section horizontal style="height: 30px">
                        <q-item-label class="col-3 bg-blue-2" flat bordered style="padding-top: 5px;">
                            <b>Analista</b>
                        </q-item-label>
                        <q-separator vertical />
                        <q-item-label class="col-6" flat bordered style="padding-top: 5px; padding-left: 3px;">
                            <div align="left">{{ usuario.nombre }} {{ usuario.apellido }}</div>
                        </q-item-label>
                    </q-card-section>
                    <q-separator horizontal />
                    <q-card-section horizontal style="height: auto; width:100%">
                        <q-item-label class="col-3 bg-blue-2" flat bordered style="padding-top: 20px; ">
                            <b>Recomendaciones</b>
                        </q-item-label>
                        <q-separator vertical />
                        <q-item-label class="col-9">
                                <q-input
                                    v-model="recomendacion"
                                    style="padding-left: 3px;"
                                    type="textarea"
                                    
                                />
                        </q-item-label>
                    </q-card-section>
                </q-card>
            </div>
            <br/>
            <q-separator inset style="width:65%"/>
            <div class="row justify-end q-gutter-sm q-ma-md" style="width:65%">
                <BotonCancelarReporte 
                    opcion="reporte"
                    @guardarAvance="guardarAvance"
                />
                <q-btn
                    
                    color="btnVolver"
                    @click="cambioAtras"
                    label=" Volver "
                    class="q-ml-sm"
                />
                <q-btn
                    class="q-ml-sm"
                    color="btnContinuar"
                    label="   Guardar Avance  "
                    @click="guardarReporte"
                />
                <q-btn
                    class="q-ml-sm"
                    color="btnAdjuntar"
                    label="   Finalizar  "
                    @click="guardarReporteFinal"
                />
            </div>
        </q-card-section>

    <q-space />
    <br/>
    </q-card>
</template>
<script>

    import { ref, toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import ReporteFuncionesEdicion from "src/components/ReporteFuncionesEdicion.vue";
    import ReporteHitosEdicion from "src/components/ReporteHitosEdicion.vue";
    import ReporteAccionesEdicion from "src/components/ReporteAccionesEdicion.vue";
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({
        components:{
            ReporteAccionesEdicion,
            ReporteFuncionesEdicion,
            ReporteHitosEdicion,
            BotonCancelarReporte,    
        },
        props: {
                usuario: Object,
                entrega: Object,
                tipoEntrega: String,
        },
        methods:{
            defineActor(rol_set){
                return rol_set[0].actor.id_uaysen
            },
            validaReporteHito(){
                if((!this.acciones.funciones.length) && (this.acciones.detalleAccion && this.acciones.detalleAccion.mdvs.length)){
                    return true;
                }else{
                    return false;
                }
            },
            validaReporteAccion(){
                if((!this.acciones.funciones.length) && (!this.acciones.detalleAccion || !this.acciones.detalleAccion.mdvs.length)){
                    return true;
                }else {
                    return false;
                }
            },
            validaFinReporte(){
                if(!(this.stepPasoAccion)){
                    return true;
                }else {
                    return false;
                }
            },
            getAccion(accion){
                if(this.acciones){
                    const idUaysen = this.acciones.detalleAccionesReporte.find(element => element.accion.id === accion);
                    return idUaysen.accion.id_uaysen;
                }
            },
        },
        setup() {
            const store = useStore();
            const router = useRouter();
            const TIMESTAMP  = Date.now();
            const fechaActual = new Date(TIMESTAMP);
            const fechaFormateada = fechaActual.toLocaleDateString();
            const anio = fechaActual.getFullYear();
            const MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",];
            const date = new Date();
            const mes = MESES[date.getMonth()];
            
            const labelBotonAtras = ref("Atra?s");
            const cambia = ref(true);
            const reporteAEditar = computed(() => store.state.reporte.aEditar);
            const accionesAReportar = computed(() => store.state.accion.acciones);
            const acciones = computed(() => store.state.accion);
            const detalleProductos = computed(() => store.state.producto.totalHitos);
            
            const Justificacion = ref('');
 
            const actor = ref('');
            const usuario = computed(() => store.state.usuarix.usuario);
            const opcionesJustificacion = ["Implementado", "No implementado", "En proceso", "Pendiente", "No aplicable", "No cumplido"];
            
            const recomendacion = ref(reporteAEditar.value.recomendacion);
            const stepPasoFuncion = ref(0);
            const stepRolSet = ref(0);
            const stepPasoHito    = ref(0);
            const stepPasoAccion = ref(0);
            const finReporteAccion = ref(false);
            const accion = ref(accionesAReportar.value.id_uaysen);
            const model = ref(reporteAEditar.value.reporte_acciones[0]);


            onMounted (() => {
                store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("reporte/setReporteAccionesAEditar",model.value);
                
            });

            const cambio = () => {
                cambia.value = false;
                
                store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                store.dispatch("producto/reqHitosReporte", model.value.accion);

                store.dispatch("reporte/setReporteHitosAEditar", model.value.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", model.value.reporte_funciones);
                accion.value = accionesAReportar.value.id_uaysen;
                store.dispatch("reporte/setReporteAccionesAEditar",model.value);
                finReporteAccion.value = false;
                cambia.value = true;
            };

            const cambioAtras = async () => {
                const reporte = {
                    id : reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "POA",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                };

                await store.dispatch("reporte/setReporteAEditar", reporte);

                model.value = reporte.reporte_acciones[0];

                store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                store.dispatch("producto/reqHitosReporte", model.value.accion);
                store.dispatch("reporte/setReporteHitosAEditar", model.value.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", model.value.reporte_funciones)

                finReporteAccion.value = false;
            };


            const validaLabelBoton = () => {
                if(model.value.reporte_funciones.length && model.value.reporte_hitos.length){
                    labelBotonAtras.value = "Volver a Funciones e Hitos";
                }else{
                    if(model.value.reporte_funciones.length && !model.value.reporte_hitos.length){
                        labelBotonAtras.value = "Volver a Funciones";
                    }else{
                        labelBotonAtras.value = "Volver a Hitos";
                    }
                }

                return true;
            };

            const cambioPasoFuncion = (data) => {
                stepPasoFuncion.value += data;
            };

            const cambioPasoHito = (data) => {
                stepPasoHito.value += data;
            };

            const cambioReporteAccion = async (reporteAccion) => {
                model.value = reporteAccion;        
            };

            const finReporte = (data) => {
                finReporteAccion.value = data;
            };

            const guardarReporte = () => {

                const reporteAGuardar = {
                    id: reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "POA",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                }

                store.dispatch("reporte/patchReporte", reporteAGuardar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const guardarReporteFinal = () => {
                
                const reporteAGuardar = {
                    id: reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Finalizado",
                    recomendacion: recomendacion.value,
                    tipo : "POA",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                }

                store.dispatch("reporte/patchReporte", reporteAGuardar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const guardarAvance = async () => {
                const reporte = {
                    id : reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "POA",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                };

                await store.dispatch("reporte/setReporteAEditar", reporte);

                store.dispatch("reporte/patchReporte", reporteAEditar.value);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };
            

            const totalFunciones = ref();
            const totalMDV = ref();
            const totalHito = ref();
            const pasoFuncion = ref(false);

            const detalleIdUaysen = computed(() => store.state.accion.detalleIdUaysen);

            const opciones = reporteAEditar.value.reporte_acciones;

            
            return {
                detalleIdUaysen,

                cambia,
                cambio,
                opciones,
                model,
                labelBotonAtras,
                guardarAvance,
                //accionesAReportar: computed(() => store.state.accion.acciones),
                actor,
                stepRolSet,
                reporteAEditar,
                detalleProductos,
                fechaFormateada,
                stepPasoAccion,
                pasoFuncion,
                finReporteAccion,
                validaLabelBoton,
                finReporte,
                cambioAtras,
                stepPasoFuncion,
                guardarReporteFinal,
                cambioPasoFuncion,
                cambioPasoHito,
                cambioReporteAccion,
                stepPasoHito,
                accionesAReportar,
                acciones,
                totalFunciones,
                totalMDV,
                totalHito,

                anio,
                mes,
                usuario,
        
                recomendacion,
                
                opcionesJustificacion,
                guardarReporte,
                
            }
        }
    })
</script>