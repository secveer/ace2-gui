// Store to track which alerts are currently selected
// Can be used in 'alert actions' modals (or elsewhere) to determine what alerts to apply actions on

import {Commit} from "vuex";

export interface CommitFunction {
    commit: Commit;
}

// EsLint says to use 'Record<string, unknown>[]' instead of 'object' type (makes for easier debugging apparently)
// Todo: convert 'Record<string, unknown>[]' type to alert interface when that's nailed down more?
// export interface Alert {
//     id: string;
// }

const store = {
    namespaced: true,
    state: {
        selected: [],
    },
    getters: {
        selected: (state: { selected: Record<string, unknown>[] }) => state.selected,
    },
    mutations: {
        SELECT: (state: { selected: Record<string, unknown>[] }, payload: Record<string, unknown>) => state.selected.push(payload),
        UNSELECT: (state: { selected: Record<string, unknown>[] }, payload: Record<string, unknown>) => (state.selected = state.selected.filter((e) => e !== payload)),
        SELECTALL: (state: { selected: Record<string, unknown>[] }, payload: Record<string, unknown>[]) => state.selected = payload,
        UNSELECTALL: (state: { selected: Record<string, unknown>[] }) => state.selected = []
    },
    actions: {
        select: ({ commit }: CommitFunction, payload: Record<string, unknown>) => commit('SELECT', payload),
        unselect: ({ commit }: CommitFunction, payload: Record<string, unknown>) => commit('UNSELECT', payload),
        selectAll: ({ commit }: CommitFunction, payload: Record<string, unknown>[]) => commit('SELECTALL', payload),
        unselectAll: ({ commit }: CommitFunction) => commit('UNSELECTALL'),
    },
}

export default store
