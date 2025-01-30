import { Injectable, signal, Signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class DialogService {
  // Signal pour contrôler l'état de la modale
  isDialogOpen = signal(false);

  // Signal pour transmettre les données soumises
  formData = signal<{ type: string; timer: number } | null>(null);

  // Ouvrir la modale
  openDialog(): void {
    this.isDialogOpen.set(true);
  }

  // Fermer la modale
  closeDialog(): void {
    this.isDialogOpen.set(false);
  }

  // Soumettre les données
  submitData(data: { type: string; timer: number }): void {
    this.formData.set(data);
    this.closeDialog();
  }
}
