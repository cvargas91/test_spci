<template>
    <div align="center">
        <q-card 
            style="width:65%"
            flat 
        >
            <p align="left">
                <b style="padding-left: 20px;">
                    2.- Evaluación Final
                </b>
            </p>
        
            <div align="center">
                <q-card-section horizontal style="height: 55px">
                    <q-item-label class="col-3 bg-blue-2" flat bordered>
                        <b>Estado de Ejecución</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col-2" flat bordered style="height: 25px">
                        <div style="height: 1px">
                            <q-select  
                                v-model="indicadorEstadoEjecucion" 
                                :options="opcionesJustificacion" 
                                style="width: 450%"
                            />
                        </div>
                    </q-item-label>
                </q-card-section>
                <q-separator horizontal />

                <q-card-section horizontal style="height: 75px"><!--  v-model="model">-->
                    <q-item-label class="col-3 bg-blue-2" flat bordered style="padding-top:4px">
                        <b>Presenta justificación por contingencia</b>
                    </q-item-label>
                    <q-separator vertical />
                
                    <q-item-section class="col-1" style="padding-top: 19px; padding-left: 2px">
                        <q-select 
                            v-model="justificacion" 
                            :options="opcionesEjecucion" 
                            style="width:100% "
                        />
                    </q-item-section>

                    <q-separator vertical />
                
                    <q-item-section class="col-4" style="height: 75px;padding-top: 19px; padding-left: 2px">
                        <div class="q-gutter-sm" style="max-width: 300px">
                            <q-input
                                v-model="reporteJustificacion"
                                autogrow
                                type="textarea"
                            />
                        </div>
                    </q-item-section>

                    <q-separator vertical />

                    <q-item-label class="col-2 bg-blue-2" flat bordered>
                        <b>Fecha Entrega reporte</b>
                    </q-item-label>
                    <q-separator vertical />
                
                    <q-item-label class="col-2" flat bordered v-model="model">
                        {{fechaFormateada}}
                    </q-item-label>
                </q-card-section>
            </div>
            <q-space />
            <br/>
            <q-separator inset />
    <div class="row justify-end q-gutter-sm q-ma-md">
        <BotonCancelarReporte 
            opcion="accion"
            @guardarAvance="guardarAvance"
        />
        <!--<q-btn
            class="q-ml-sm"
            color="btnCancelar"
            label="   Cancelar   "
            @click="cancelarReporte"
        />-->
    
        <q-btn
            v-if="validaLabelBoton()"
            color="btnVolver"
            @click="cambioAtras"
            :label="labelBotonAtras"
            class="q-ml-sm"
        />
        <q-btn
            color="btnContinuar"
            @click="cambioAdelante"
            label="   Continuar    "
            class="q-ml-sm"
        />
    </div>
        <q-space />
        <br/>
    </q-card>
</div>
</template>
<script>
    import { ref,toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
        },
        props:{
            fechaFormateada: String,
            opcionesJustificacion: Array,
            reporteAccion: Object,
        },
        watch: {
            reporteAccion: async function(newValue, oldValue) {
                
                const reporteAccion = {
                    accion: oldValue.accion,
                    estado_ejecucion: this.indicadorEstadoEjecucion,
                    justificacion_contingencia: this.justificacion,
                    reporte_justificacion_contingencia: this.reporteJustificacion,
                    reporte_funciones: oldValue.reporte_funciones,
                    reporte_hitos: oldValue.reporte_hitos
                };

                await this.$store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);
            },
        },
        emits:["cambioReporteAccion","finReporte"],
        setup(props, {emit}) {        
            const store = useStore();     
            const router = useRouter();
            const accion = computed(() => store.state.accion);
            const accionesAReportar = ref('');
            const reportes = computed(() => store.state.reporte);
            const opcionesEjecucion = ["Si", "No"];
            
            const labelBotonAtras = ref("Atras");

            const indicadorEstadoEjecucion = ref(props.reporteAccion.estado_ejecucion);
            const reporteJustificacion = ref(props.reporteAccion.reporte_justificacion_contingencia);
            const justificacion = ref(props.reporteAccion.justificacion_contingencia);
            const idAccion = ref(props.reporteAccion.accion);
            const pasoAccion = ref(0);

            const model = computed({
                get:() => {
                
                    idAccion.value = props.reporteAccion.accion;
                    indicadorEstadoEjecucion.value = props.reporteAccion.estado_ejecucion;
                    justificacion.value = props.reporteAccion.justificacion_contingencia;
                    reporteJustificacion.value = props.reporteAccion.reporte_justificacion_contingencia;   
                }
            })

            const cambioAdelante = async () => {
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);
                emit('finReporte', true);
            };

            const cambioAtras = async () => {
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar
                };                

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);

                store.dispatch("accion/reqDetalleAccion", idAccion.value);
                store.dispatch("accion/reqFuncionesPorAccion", idAccion.value);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", idAccion.value);
                store.dispatch("producto/reqHitosReporte", idAccion.value);
                store.dispatch("reporte/setReporteHitosAEditar", props.reporteAccion.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", props.reporteAccion.reporte_funciones)

                emit('cambioReporteAccion', reporteAccion);
            };

            const validaLabelBoton = () => {
                if(props.reporteAccion.reporte_funciones.length && props.reporteAccion.reporte_hitos.length){
                    labelBotonAtras.value = "Volver a Funciones e Hitos";
                }else{
                    if(props.reporteAccion.reporte_funciones.length && !props.reporteAccion.reporte_hitos.length){
                        labelBotonAtras.value = "Volver a Funciones";
                    }else{
                        labelBotonAtras.value = "Volver a Hitos";
                    }
                }

                return true;
            };

            const guardarAvance = async () => {

                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);


                store.dispatch("reporte/patchReporte", reportes.value.aEditar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };


            return {
                cambioAdelante,
                cambioAtras,
                reportes,
                guardarAvance,

                validaLabelBoton,
                model,
                accionesAReportar,
                idAccion,
                accion,
                labelBotonAtras,
                opcionesJustificacion: toRef(props,"opcionesJustificacion"),
                opcionesEjecucion,
                reporteAccion: toRef(props, "reporteAccion"),
                justificacion,
                
                indicadorEstadoEjecucion,

                reporteJustificacion,
                fechaFormateada: toRef(props, "fechaFormateada"),
            }
        }
    })
</script>