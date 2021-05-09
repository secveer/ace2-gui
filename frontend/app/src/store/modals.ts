// https://xon5.medium.com/a-vue-modal-manager-via-vuex-1ae530c8649

// todo: need to come back and give these proper types, rather than anys
const store = {
    namespaced: true,
    state: {
        open: [],
    },
    getters: {
        active: (state: { open: string | any[] }) => (state.open.length > 0 ? state.open[0] : null),
        allOpen: (state: { open: any }) => state.open,
    },
    mutations: {
        OPEN: (state: { open: any[] }, payload: any) => state.open.unshift(payload),
        CLOSE: (state: { open: any[] }, payload: any) => (state.open = state.open.filter((e) => e !== payload)),
    },
    actions: {
        open: ({ commit }: any, payload: any) => commit('OPEN', payload),
        close: ({ commit }: any, payload: any) => commit('CLOSE', payload),
    },
}

export default store
