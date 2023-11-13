import {Component} from '@angular/core';
import {DialogRef} from "@angular/cdk/dialog";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-order-dialog',
  templateUrl: './order-dialog.component.html',
  styleUrls: ['./order-dialog.component.scss']
})
export class OrderDialogComponent {

  public method: string = '';
  public contact: string = '';

  constructor(private dialogRef: DialogRef,
              private snackBar: MatSnackBar) {
  }

  public close(): void {
    this.snackBar.open('Ваши данные отправлены, в скором времени с вами свяжется наш менеджер', 'Хорошо');
    this.dialogRef.close({
      method: this.method,
      contact: this.contact
    });
  }
}
