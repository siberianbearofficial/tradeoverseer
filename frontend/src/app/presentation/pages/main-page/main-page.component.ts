import {Component} from '@angular/core';
import {Dialog} from "@angular/cdk/dialog";
import {OrderDialogComponent} from "../../shared/components/order-dialog/order-dialog.component";
import {Observable, of, switchMap} from "rxjs";
import {Order} from "../../../core/domain/entities/order";
import {OrderService} from "../../../core/usecases/interactors/order.service";

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent {
  protected readonly window = window;

  constructor(private dialog: Dialog,
              private orderService: OrderService) {
  }

  public showOrderDialog(selected: string): void {
    this.dialog.open(OrderDialogComponent).closed.pipe(
      switchMap((result): Observable<void> => {
        (result as Order).selected = selected;
        if (result && (result as Order).contact)
          return this.orderService.sendOrder(result as Order);
        return of(void 0);
      })).subscribe();
  }
}
