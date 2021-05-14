import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import {shallowMount, mount, VueWrapper} from "@vue/test-utils";


describe("TheAlertsTable.vue", () => {
    // @ts-ignore
    const wrapper = mount(TheAlertsTable);

    it("renders", () => {
        expect(wrapper.exists()).toBe(true);
    });

})