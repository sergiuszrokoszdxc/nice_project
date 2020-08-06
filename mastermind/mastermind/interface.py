  

    def guess(self, proposed_sequence):
        if self._n_tries < self._max_tries:
            try:
                self._validate(proposed_sequence)
            except ValueError:
                return_string = "Proposed sequence is not valid."
            else:
                self._n_tries += 1
                hints = self._guess(proposed_sequence)
                return_string = self._build_hint_string(hints)
        else:
            return_string = "Max number of tries attained"
        return return_string


        

    def _build_hint_string(self, hints):
        if hints[0] == self._n_pos:
            if self._n_tries == 1:
                msg = f"Congratulations. You succeeded in {self._n_tries} try."
            else:
                msg = f"Congratulations. You succeeded in {self._n_tries} tries."
        else:
            msg = (
                f"{hints[0]} pins are in correct position. "
                "{hints[1]} pins are in correct colour. "
            )
            tries_left = self.tries_left
            if tries_left == 1:
                msg += "1 try left."
            else:
                msg += f"{self.tries_left} tries left."
        return msg