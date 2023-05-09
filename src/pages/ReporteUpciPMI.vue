<template>
    <q-card 
        class="my-card" 
        align="center"
        flat bordered
        v-if="dataReady"
        style="height:770pt"
    >
        <q-card-actions align="around" style="padding-bottom:0pt" >
                <div style="padding-left:40pt">
                    <p style="margin-top:5pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:11pt">
                        <strong>Reporte Medios de Verificación</strong>                        
                    </p>
                    <p style="margin-top:0pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:8pt">
                        Plan de Mejora Institucional
                    </p>
                    <p style="margin-top:0pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:7pt">
                            <span style="background-color:#d9e2f3"> 
                                {{mes}} 2022
                            </span>
                    </p>
                </div>
                <q-card-section horizontal style="padding-right:30pt">
                    <div style="margin-top:9pt; margin-right:5pt">
                        <img 
                            id="logo"
                            src="/static/webapp/Colabora-logo_recortado.png"
                            name="image1.jpg" 
                            align="center" 
                            width="140" 
                            height="30" 
                        />
                        <p align="center" style="color:#385280; font-size:5pt;padding-left:4pt; padding-top:0pt">
                            Plataforma de Planificación y Coordinación <br/>
                                Institucional UAysén
                        </p>
                    </div>
                    
                        <img 
                            id="logo"
                            src="/static/webapp/uaysen-nuevo-1.png"
                            name="image1.jpg" 
                            width="50" 
                            height="50" 
                            style="margin-top:9pt; margin-right:5pt"
                        />
                </q-card-section>    
        </q-card-actions>
        <hr style="border: 1.5px dashed #385280; margin-right:178pt; margin-left:178pt; padding-top:0pt;">
        
        <q-card style="margin-right:0pt; margin-left:0pt; width:100%; padding-top:0%;padding-bottom:36pt">
            <q-card-section style="padding-bottom:0pt">
                <strong style="text-align:center; color:#385280; font-size:12pt">
                    Título Acción de Mejora:
                </strong>  <br/>
                <div style="background-color:#fcefd5;width:560pt; margin-right:0pt; margin-left:0pt; min-height:10pt; padding-right:40pt">
                    <p style="color:#385280; font-size:10pt; padding-top:3pt;padding-bottom:0pt;text-align:center; margin-left:30pt">
                        <b>{{accionesAReportar.titulo}}</b>
                    </p>
                </div>  
                <strong style="text-align:center; color:#385280; font-size:10pt">
                    Identificador Acción de Mejora:
                </strong>   
                <div style="background-color:#fcefd5;width:560pt; margin-right:0pt; margin-left:0pt; min-height:10pt; padding-right:40pt">
                    <q-select
                        v-model="model"
                        :options="opciones"
                        :option-label="(item) => item === null ? 'Null' : getAccion(item.accion)"
                        @update:model-value="cambio"
                        style="width: 100%; height:100%; margin-left:10pt; margin-bottom:30pt"
                        item-aligned 
                    />
                    
                </div>
            </q-card-section>

            <q-card-section horizontal>
                <p style="padding-left:24%">
                    <strong style="text-align:center; color:#385280; font-size:10pt">
                        Responsable Ejecutivo
                    </strong>   
                </p>
                <p style="padding-left:25%">
                    <strong style="text-align:center; color:#385280; font-size:10pt; align-right">
                        Responsable Estratégico
                    </strong>  
                </p>
            </q-card-section>

            <q-card-section horizontal>
                <div style="background-color:#fcefd5;width:30%; margin-left:20%; min-height:30pt; margin-right:0pt">
                    <p style="text-align:center; color:#385280; font-size:10pt;padding-top:7pt;padding-right:22pt">
                        {{defineActor(accionesAReportar.rol_set)}}
                    </p>   
                </div>
                
                <div style="background-color:#fcefd5;width:30%;min-height:25pt;margin-left:3pt;margin-right:40pt">
                    <p style="text-align:center; color:#385280; font-size:10pt;padding-top:5pt">
                        {{defineActorEstrategico(accionesAReportar.rol_set)}}
                    </p>   
                </div>
            </q-card-section>

            <q-card-section style="height:40pt; padding-top:1%;margin-bottom:26pt">
                <strong style="text-align:center; color:#385280; font-size:10pt">
                    MdV Acción de Mejora:
                </strong>   
                <div style="background-color:#d9e2f3; width:560pt; margin-right:0pt; margin-left:0pt; min-height:15pt; padding-right:40pt">
                    <p style="color:#385280; font-size:10pt; padding-top:3pt;padding-bottom:0pt;text-align:center; margin-left:30pt; margin-top:4pt; margin-bottom:4pt">
                        <b>{{acciones.funciones[0].indicador_set[0].nombreVerificador}}</b>
                    </p>    
                </div>
            </q-card-section>
        </q-card>
        
        <hr style="border: 1.5px dashed #385280; margin-right:191pt; margin-left:178pt">
        <br/>
        <q-card-section style="margin-right:178pt; margin-left:165pt; height:30pt; margin-bottom:0pt;margin-top:0pt; padding-top:0%;padding-bottom:0pt">
            <div class="row" style="border: solid #385280; border-width:0.5px; margin-left:2pt;margin-right:98pt" v-if="validaReporteHitoPMI()">
                <p style="color:#385280; margin-bottom:4pt;padding-top:4pt; padding-right:165pt;padding-left:5pt">
                    <b>1.- Evaluación entrega a Medios de Verificación</b>
                </p>            
            </div>
            <ReporteHitosPMI
                :identificador="accionesAReportar.id_uaysen"
                :mdvs="acciones.detalleAccion.mdvs"
                :hitos="acciones.detalleAccion.hitos"
                :reporteAccion="model"
                :fechaFormateada="fechaFormateada"
                :funciones="acciones.funciones"
                v-if="validaReporteHitoPMI()"  
            />
        </q-card-section>
        
        
        <q-card-section style="margin-right:178pt; margin-left:165pt; height:30pt; margin-bottom:0pt;margin-top:0%; padding-top:0%;padding-bottom:0pt">
            <div class="row" style="border: solid #385280; border-width:0.5px; margin-left:2pt;margin-right:98pt" v-if="validaReporteAccionPMI()">
                <p style="color:#385280; margin-bottom:4pt;padding-top:0pt; padding-right:165pt;padding-left:5pt">
                    <b>2.- Resultados</b>
                </p>            
            </div>  
            <ReporteAccionesPMI 
                :opcionesJustificacion="opcionesJustificacion"
                :indiceReporteAccion="indiceReporteAccion"
                :reporteAccion="model"
                :funciones="acciones.funciones"
                @cambioReporteAccion="cambioReporteAccion"
                @guardarReporte="guardarReporte"
                @siguienteReporteAccion="siguienteReporteAccion"
                v-if="validaReporteAccionPMI()"
            />
        </q-card-section>

    </q-card>
    <br/>
    <br/>
    <br/>
    <br/>
</template>
<script>

    import { ref, toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";
    import ReporteHitosPMI from "src/components/ReporteHitosPMI.vue";
    import ReporteAccionesPMI from "src/components/ReporteAccionesPMI.vue";

    export default defineComponent({
        components:{                    
            BotonCancelarReporte,
            ReporteHitosPMI,
            ReporteAccionesPMI,
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
            defineActorEstrategico(rol_set){
                let estrategico = this.actores.find(element => element.id === rol_set[0].actor.dependencia);
                return estrategico.id_uaysen
            },
            validaReporteHitoPMI()  {
                if((this.acciones.detalleAccion && this.acciones.detalleAccion.mdvs.length)){
                    return true;
                }else{
                    return false;
                }
            },
            validaReporteAccionPMI(){
                
                if((!this.acciones.detalleAccion || !this.acciones.detalleAccion.mdvs.length)){
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
                if(this.acciones.detalleAccionesReporte){
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
            const actores = computed(() => store.state.actor.actores);
            const reporte = computed(() => store.state.reporte);
            const accionesAReportar = computed(() => store.state.accion.acciones);
            //const funcion = computed(() => store.state)
            const acciones = computed(() => store.state.accion);
            const detalleProductos = computed(() => store.state.producto.totalHitos);

            const model = ref(reporte.value.nuevoReporte.reporte_acciones[0]);
            const indiceReporteAccion = ref(0);

            const usuario = computed(() => store.state.usuarix.usuario);
            const opcionesJustificacion = ["Implementado", "No implementado", "En proceso", "Pendiente", "No aplicable", "No cumplido"];
            const dataReady = ref(false);
            const recomendacion = ref(reporte.value.nuevoReporte.recomendacion);
            const stepPasoFuncion = ref(0);
            const stepPasoHito    = ref(0);
            const stepPasoAccion = ref(0);
            const finReporteAccion = ref(false);
            
            const reporteFuncion = {
                id_tactica : "F01",
                funcion : "",
                indicador : 0,
                comentario_cumplimiento : ""
            };

            onMounted( async () => {
                await store.dispatch("accion/reqDetalleAccion", model.value.accion);
              //  await 
                store.dispatch("reporte/setNuevoReporteHito", reporte.value.nuevoReporte.reporte_acciones[0].reporte_hitos);
              //  await 
                await store.dispatch("reporte/setNuevoReporteFuncion", reporte.value.nuevoReporte.reporte_acciones[0].reporte_funciones);

                dataReady.value = true;
            });

            const cambio = async () => {
                indiceReporteAccion.value = getIndex(model.value.accion);

                await store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                store.dispatch("producto/reqHitosReporte", model.value.accion);
                
                store.dispatch("reporte/setNuevoReporteHito", model.value.reporte_hitos);
                store.dispatch("reporte/setNuevoReporteFuncion", model.value.reporte_funciones);
            };

            const getIndex = (accion) => {
                return reporte.value.nuevoReporte.reporte_acciones.map(object => object.accion).indexOf(accion);
            };
        

            const cambioReporteAccion = async (reporteAccion) => {
                model.value = reporteAccion;
            };

            const siguienteReporteAccion = async (indice) => {
                model.value = reporte.value.nuevoReporte.reporte_acciones[indice];
                cambio();
            };

            const finReporte = (data) => {
                finReporteAccion.value = data;
            };

            const guardarAvance = async () => {
                const nuevoReporte = {
                    usuario: usuario.value.id,
                    actor: reporte.value.nuevoReporte.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "PMI",
                    reporte_acciones: reporte.value.nuevoReporte.reporte_acciones
                };

                store.dispatch("reporte/postReporte", nuevoReporte);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                await store.dispatch("reporte/reqReportesBorradores");
                await store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            }

            const cambioAtras = async () => {
                const nuevoReporte = {
                    //id : reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporte.value.nuevoReporte.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "PMI",
                    reporte_acciones: reporte.value.nuevoReporte.reporte_acciones
                };

                await store.dispatch("reporte/actalizaNuevoReporte", nuevoReporte);

                model.value = reporte.value.nuevoReporte.reporte_acciones[0];
                store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                store.dispatch("producto/reqHitosReporte", model.value.accion);
                store.dispatch("reporte/setReporteHitosAEditar", model.value.reporte_hitos);
                //store.dispatch("reporte/setReporteFuncionesAEditar", model.value.reporte_funciones)
                finReporteAccion.value = false;
            };


            const guardarReporte = () => {
                const reporteAGuardar = {
                    usuario: usuario.value.id,
                    actor: reporte.value.nuevoReporte.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "PMI",
                    reporte_acciones: reporte.value.nuevoReporte.reporte_acciones
                }

                store.dispatch("reporte/postReporte", reporteAGuardar);
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

            const opciones = reporte.value.nuevoReporte.reporte_acciones;

            return {
                indiceReporteAccion,
                detalleIdUaysen,
                actores,
                opciones,
                model,
                cambio,
                reporte,
                dataReady,
                cambioReporteAccion,
                finReporte,
                siguienteReporteAccion,
                cambioAtras,
                guardarAvance,

                detalleProductos,
                fechaFormateada,
                stepPasoAccion,
                pasoFuncion,
                finReporteAccion,

                stepPasoFuncion,
    
                stepPasoHito,

                acciones,
                totalFunciones,
                totalMDV,
                totalHito,

                anio,
                mes,
                accionesAReportar,
                usuario,

                recomendacion,
                opcionesJustificacion,
                guardarReporte,
            }
            
        }
    })
</script>