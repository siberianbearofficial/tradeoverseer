import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {MainPageComponent} from "./presentation/pages/main-page/main-page.component";

const routes: Routes = [
  {path: '', component: MainPageComponent, title: 'TradeOverseer'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
