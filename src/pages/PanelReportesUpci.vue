<template>
    <div class="q-pa-md" style="height:auto;flex-grow:1" >
        <q-card 
            class="my-card"
        >
            <!--v-model="tab"-->
            <q-tabs
                :model-value="tab"
                @update:model-value="cambiaTab"
                dense
                active-color="primary"
                indicator-color="primary"
                align="justify"
                class="tablaAcciones"
            >
                <q-tab name="POA" label="Plan Operativo Anual" />
                <q-tab name="PMI" label="Plan de Mejora Institucional" />
            </q-tabs>

            <q-separator />
            <q-tab-panels v-model="tab" animated>
                <q-tab-panel name="POA" class="q-pa-none">
                    <q-splitter
                        v-model="splitterModel"
                        style="height: 518px"
                    >
                        <template v-slot:before>
                            <q-tabs
                                v-model="innerTab"
                                vertical
                                class="text-teal"
                            >
                                <q-tab name="reporte">
                                    <q-avatar  
                                        icon="description"
                                        size="md"
                                        color="light-blue-10"
                                        text-color="white"
                                    />
                                        <b>Generar</b>
                                </q-tab>
                                <q-tab name="borradores">
                                    <!--draft-->
                                    <q-avatar
                                        icon="edit_note"
                                        size="md"
                                        color="light-blue-10"
                                        text-color="white"
                                    />
                                    <b>Borradores</b>
                                </q-tab>
                                <q-tab name="finalizados">
                                    <q-avatar
                                    icon="task"
                                    size="md"
                                    color="light-blue-10"
                                    text-color="white"
                                />
                                <b>Finalizados</b>
                            </q-tab>
                            </q-tabs>
                        </template>

                        <template v-slot:after>
                            <q-tab-panels class="text-textoAzul"
                                v-model="innerTab"
                                animated
                                swipeable
                                vertical
                                transition-prev="jump-up"
                                transition-next="jump-up"
                                >
                                <q-tab-panel name="reporte">
                                    <div class="text-h4 q-mb-md">
                                        <b> Generar Reporte POA</b>
                                    </div>
                                        <BandejaUnidades
                                            origen="POA"
                                            :reportes="reportes.finalizado"
                                        />   
                                </q-tab-panel>
        
                                <q-tab-panel name="borradores">
                                    <div class="text-h4 q-mb-md">
                                        <b> Borradores POA </b>
                                    </div>
                                    <BandejaReportes
                                        :reportes="reportes.borrador"/>
                                </q-tab-panel>
        
                                <q-tab-panel name="finalizados">
                                    <div class="text-h4 q-mb-md">
                                        <b> Finalizados POA</b>
                                    </div>
                                    <BandejaReportes
                                        :reportes="reportes.finalizado"/>
                                </q-tab-panel>
                            </q-tab-panels>
                        </template>
                    </q-splitter>
                </q-tab-panel>
                
                <q-tab-panel name="PMI" class="q-pa-none">
                    <q-splitter
                        v-model="splitterModel"
                        style="height: 518px"
                    >
                        <template v-slot:before>
                            <q-tabs
                                v-model="innerTab"
                                vertical
                                class="text-teal"
                            >
                                <q-tab name="reporte">
                                    <q-avatar  
                                        icon="description"
                                        size="md"
                                        color="light-blue-10"
                                        text-color="white"
                                    />
                                        <b>Generar</b>
                                </q-tab>
                                <q-tab name="borradores">
                                    <!--draft-->
                                    <q-avatar
                                        icon="edit_note"
                                        size="md"
                                        color="light-blue-10"
                                        text-color="white"
                                    />
                                    <b>Borradores</b>
                                </q-tab>
                                <q-tab name="finalizados">
                                    <q-avatar
                                    icon="task"
                                    size="md"
                                    color="light-blue-10"
                                    text-color="white"
                                />
                                <b>Finalizados</b>
                            </q-tab>
                            </q-tabs>
                        </template>

                        <template v-slot:after>
                            <q-tab-panels class="text-textoAzul"
                                v-model="innerTab"
                                animated
                                swipeable
                                vertical
                                transition-prev="jump-up"
                                transition-next="jump-up"
                                >
                                <q-tab-panel name="reporte">
                                    <div class="text-h4 q-mb-md">
                                        <b> Generar Reporte PMI</b>
                                    </div>
                                        <BandejaUnidades
                                            origen="PMI"
                                            :reportes="reportes.finalizadoPMI"
                                        />                                                                    
                                </q-tab-panel>
        
                                <q-tab-panel name="borradores">
                                    <div class="text-h4 q-mb-md">
                                        <b> Borradores PMI</b>
                                    </div>
                                    <BandejaReportes
                                        :reportes="reportes.borradorPMI"/>
                                </q-tab-panel>
        
                                <q-tab-panel name="finalizados">
                                    <div class="text-h4 q-mb-md">
                                        <b> Finalizados PMI</b>
                                    </div>
                                    <BandejaReportes
                                        :reportes="reportes.finalizadoPMI"
                                    />
                                </q-tab-panel>
                            </q-tab-panels>
                        </template>
                    </q-splitter>
                    
                </q-tab-panel>
            </q-tab-panels>
            
            <!--<q-splitter
                v-model="splitterModel"
                style="height: 650px"
                >
                <template v-slot:before>
                    <q-tabs
                        v-model="tab"
                        vertical
                        class="text-teal"
                    >
                        <q-tab name="reporte">
                            <q-avatar  
                                icon="description"
                                size="md"
                                color="light-blue-10"
                                text-color="white"
                            />
                            <b>Generar Reporte</b>
                        </q-tab>
                        <q-tab name="borradores">
                            <!-draft--
                            <q-avatar
                                icon="edit_note"
                                size="md"
                                color="light-blue-10"
                                text-color="white"
                            />
                            <b>Borrador Reportes</b>
                        </q-tab>
                        <q-tab name="finalizados">
                                <q-avatar
                                icon="task"
                                size="md"
                                color="light-blue-10"
                                text-color="white"
                            />
                            <b>Reportes Finalizados</b>
                        </q-tab>
                    </q-tabs>
                </template>

                <template v-slot:after>
                    <q-tab-panels class="text-textoAzul"
                        v-model="tab"
                        animated
                        swipeable
                        vertical
                        transition-prev="jump-up"
                        transition-next="jump-up"
                        >
                        <q-tab-panel name="reporte">
                            <div class="text-h4 q-mb-md"><b> Generar Reporte</b></div>
                                <BandejaUnidades/>                            
                        </q-tab-panel>

                        <q-tab-panel name="borradores">
                            <div class="text-h4 q-mb-md"><b> Borradores </b></div>
                            <BandejaReportes
                                :reportes="reportes.borrador.borradores"/>
                        </q-tab-panel>

                        <q-tab-panel name="finalizados">
                            <div class="text-h4 q-mb-md"><b> Finalizados </b></div>
                            <BandejaReportes
                                :reportes="reportes.finalizado.finalizados"/>
                        </q-tab-panel>
                    </q-tab-panels>
                </template>

            </q-splitter>-->            
        </q-card>        
    </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import BandejaUnidades from "src/components/BandejaUnidades.vue";
import BandejaReportes from "src/components/BandejaReportes.vue";

export default {
    components:{
    BandejaUnidades,
    BandejaReportes,
},
    setup() {
        const store = useStore();
        const reportes = computed (() => store.state.reporte);
        const reportes2 = computed (() => store.state.reporte.reporte);
        const repoBorradores = computed (() => store.state.reporte.reporte.borradores);

        const tab = ref("POA");
        const innerTab =  ref("reporte");

        const cambiaTab = (value, event) => {
            if(value === "POA"){
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
            }else{
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
            }
            store.dispatch("reporte/limpiaReporteAEditar");
            store.dispatch("accion/limpiaAccionAReportar");
            store.dispatch("reporte/limpiaReporteAccion");
            tab.value = value;
            innerTab.value = "reporte";
        };
        //onMounted(() => {
            store.dispatch("reporte/reqReportesBorradores");
            store.dispatch("reporte/reqReportesUpci");
            store.dispatch("reporte/limpiaReporteAEditar");
            store.dispatch("accion/limpiaAccionAReportar");
            store.dispatch("reporte/limpiaReporteAccion");
        //});        
        return {
            reportes,
            reportes2,
            
            splitterModel: ref(20),
            cambiaTab,
            tab,
            innerTab,
    }
    },
}
</script>