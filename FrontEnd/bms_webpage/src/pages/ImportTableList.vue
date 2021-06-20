<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-100 md-size-66">
        <new-import-form data-background-color="green"></new-import-form>
      </div>
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">进货管理</h4>
            <p class="category"></p>
          </md-card-header>
          <md-card-content>
            <import-table table-header-color="green"></import-table>
          </md-card-content>
        </md-card>
      </div>

      <!--<div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">进货管理员</h4>
            <p class="category">Here is a subtitle for this table</p>
          </md-card-header>
          <md-card-content>
            <ordered-table></ordered-table>
          </md-card-content>
        </md-card>
      </div>-->
    </div>
  </div>
</template>

<script>
import { NewImportForm } from "@/pages";
import { ImportTable } from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  components: {
    ImportTable,
    NewImportForm
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.role = Cookies.get("role");
        if (this.role != "0" && this.role != "2") {
          this.$router.replace({
            path: "/login"
          });
        }
      }, //Error callback
      response => {
        if (response.status != 200) {
          this.$router.replace({
            path: "/login"
          });
        }
      }
    );
  }
};
</script>
