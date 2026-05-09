import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import random
import os
import sys

# ── colori e font ────────────────────────────────────────────────────────────
BG         = "#1e1e2e"
CARD_BG    = "#2a2a3e"
ACCENT     = "#7c6af7"
ACCENT2    = "#5e5bd8"
TEXT       = "#e0e0f0"
TEXT_DIM   = "#9090b0"
GREEN      = "#4ade80"
YELLOW     = "#facc15"
RED        = "#f87171"
WHITE      = "#ffffff"
BTN_HOVER  = "#6356e0"

# varianti scure per sfondi (no alpha, tkinter non le supporta)
GREEN_DK   = "#1a3d2b"
GREEN_MID  = "#2a6644"
YELLOW_DK  = "#3d3010"
YELLOW_MID = "#6b540f"
RED_DK     = "#3d1a1a"
RED_MID    = "#662a2a"
ACCENT_DK  = "#2a2060"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_H2     = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 12)
FONT_SMALL  = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 11, "bold")


# ── helpers ──────────────────────────────────────────────────────────────────

def resource_path(relative_path):
    """Risolve il path sia in sviluppo sia in bundle PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def load_questions(path: str) -> list[dict]:
    df = pd.read_excel(path, header=0)
    df.columns = ["num", "domanda", "efficace", "media", "non_efficace"]
    questions = []
    for _, row in df.iterrows():
        questions.append({
            "num": int(row["num"]),
            "domanda": str(row["domanda"]).strip(),
            "efficace": str(row["efficace"]).strip(),
            "media": str(row["media"]).strip(),
            "non_efficace": str(row["non_efficace"]).strip(),
        })
    return questions


# ── widget personalizzati ─────────────────────────────────────────────────────

class HoverButton(tk.Label):
    """Bottone con hover effect puro tkinter."""
    def __init__(self, parent, text, command=None, bg=ACCENT, fg=WHITE,
                 font=FONT_BTN, padx=20, pady=10, radius=8, **kwargs):
        super().__init__(parent, text=text, bg=bg, fg=fg, font=font,
                         padx=padx, pady=pady, cursor="hand2", **kwargs)
        self._bg      = bg
        self._command = command
        self.bind("<Enter>",    lambda e: self.config(bg=BTN_HOVER))
        self.bind("<Leave>",    lambda e: self.config(bg=self._bg))
        self.bind("<Button-1>", lambda e: command() if command else None)

    def update_command(self, command):
        self._command = command
        self.bind("<Button-1>", lambda e: command() if command else None)


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        canvas     = tk.Canvas(self, bg=BG, highlightthickness=0)
        scrollbar  = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=BG)

        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left",  fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


# ── schermata BENVENUTO ───────────────────────────────────────────────────────

class WelcomeScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🎓", font=("Segoe UI", 48), bg=BG, fg=ACCENT).pack(pady=(60, 0))
        tk.Label(self, text="Quiz Simulator", font=FONT_TITLE, bg=BG, fg=WHITE).pack(pady=(10, 4))
        tk.Label(self, text="Carica il file Excel e inizia il tuo allenamento",
                 font=FONT_BODY, bg=BG, fg=TEXT_DIM).pack(pady=(0, 40))

        # card
        card = tk.Frame(self, bg=CARD_BG, padx=30, pady=30)
        card.pack(padx=60, pady=0, ipadx=10, ipady=10)

        # file row
        file_row = tk.Frame(card, bg=CARD_BG)
        file_row.pack(fill="x", pady=(0, 20))
        tk.Label(file_row, text="File Excel:", font=FONT_BODY, bg=CARD_BG, fg=TEXT).pack(side="left")
        self.file_label = tk.Label(file_row, text="Nessun file selezionato",
                                   font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM)
        self.file_label.pack(side="left", padx=10)
        HoverButton(file_row, text="📂 Sfoglia", command=self._browse,
                    bg="#3a3a55", pady=6).pack(side="right")

        # num domande
        num_row = tk.Frame(card, bg=CARD_BG)
        num_row.pack(fill="x", pady=(0, 20))
        tk.Label(num_row, text="Numero di domande:", font=FONT_BODY, bg=CARD_BG, fg=TEXT).pack(side="left")
        self.num_var = tk.StringVar(value="10")
        spin = tk.Spinbox(num_row, from_=1, to=500, textvariable=self.num_var,
                          width=5, font=FONT_BODY, bg=CARD_BG, fg=TEXT,
                          buttonbackground=ACCENT, relief="flat",
                          insertbackground=TEXT)
        spin.pack(side="right")

        # modalità
        mode_row = tk.Frame(card, bg=CARD_BG)
        mode_row.pack(fill="x", pady=(0, 10))
        tk.Label(mode_row, text="Modalità:", font=FONT_BODY, bg=CARD_BG, fg=TEXT).pack(side="left")
        self.mode_var = tk.StringVar(value="quiz")
        modes = [("🏆 Quiz", "quiz"), ("📖 Studio", "studio")]
        for label, val in modes:
            rb = tk.Radiobutton(mode_row, text=label, variable=self.mode_var, value=val,
                                font=FONT_BODY, bg=CARD_BG, fg=TEXT,
                                selectcolor=ACCENT, activebackground=CARD_BG,
                                activeforeground=WHITE)
            rb.pack(side="right", padx=8)

        # bottone avvia
        HoverButton(self, text="▶  Inizia", command=self._start,
                    pady=12, padx=40, font=("Segoe UI", 13, "bold")).pack(pady=30)

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            self.app.excel_path = path
            self.file_label.config(text=os.path.basename(path), fg=GREEN)

    def _start(self):
        if not hasattr(self.app, "excel_path") or not self.app.excel_path:
            messagebox.showerror("Errore", "Seleziona prima un file Excel.")
            return
        try:
            n = int(self.num_var.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero valido di domande.")
            return
        try:
            all_q = load_questions(self.app.excel_path)
        except Exception as ex:
            messagebox.showerror("Errore nel file", str(ex))
            return
        if n > len(all_q):
            n = len(all_q)
        selected = random.sample(all_q, n)
        self.app.start_quiz(selected, self.mode_var.get())


# ── schermata QUIZ ────────────────────────────────────────────────────────────

class QuizScreen(tk.Frame):
    SCORE_MAP = {"efficace": 1.0, "media": 0.5, "non_efficace": 0.0}

    def __init__(self, master, app, questions: list[dict], mode: str):
        super().__init__(master, bg=BG)
        self.app        = app
        self.questions  = questions
        self.mode       = mode          # "quiz" | "studio"
        self.idx        = 0
        self.score      = 0.0
        self.answers    = []            # list of (q, chosen_key, correct=True/False)
        self._build()
        self._show_question()

    # ── layout ─────────────────────────────────────────────────────────────
    def _build(self):
        # ── header fisso in cima ────────────────────────────────────────────
        hdr = tk.Frame(self, bg=CARD_BG, pady=12)
        hdr.pack(fill="x", side="top")

        left = tk.Frame(hdr, bg=CARD_BG)
        left.pack(side="left", padx=20)
        self.mode_badge = tk.Label(left, text="", font=FONT_SMALL,
                                   bg=ACCENT, fg=WHITE, padx=8, pady=3)
        self.mode_badge.pack(side="left")
        self.prog_label = tk.Label(left, text="", font=FONT_SMALL,
                                   bg=CARD_BG, fg=TEXT_DIM)
        self.prog_label.pack(side="left", padx=12)

        right = tk.Frame(hdr, bg=CARD_BG)
        right.pack(side="right", padx=20)
        tk.Label(right, text="Punteggio:", font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM).pack(side="left")
        self.score_label = tk.Label(right, text="0.0", font=FONT_H2, bg=CARD_BG, fg=ACCENT)
        self.score_label.pack(side="left", padx=4)

        # progress bar
        self.pb_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Quiz.Horizontal.TProgressbar",
                        troughcolor=CARD_BG, background=ACCENT,
                        thickness=6, bordercolor=BG)
        self.pb = ttk.Progressbar(self, variable=self.pb_var,
                                   style="Quiz.Horizontal.TProgressbar",
                                   maximum=len(self.questions))
        self.pb.pack(fill="x", side="top")

        # ── barra inferiore fissa con bottone ───────────────────────────────
        self.bottom_bar = tk.Frame(self, bg=CARD_BG, pady=10)
        self.bottom_bar.pack(fill="x", side="bottom")

        # badge tipo risposta (mostrato dopo la scelta)
        self.result_badge = tk.Label(self.bottom_bar, text="", font=FONT_H2,
                                     bg=CARD_BG, fg=WHITE, padx=16)
        self.result_badge.pack(side="left", padx=(20, 0))

        self.next_btn = HoverButton(self.bottom_bar, text="Prossima  →",
                                    command=self._next, pady=8, padx=28)
        self.next_btn.pack(side="right", padx=20)
        self.next_btn.pack_forget()

        # ── area scrollabile ────────────────────────────────────────────────
        self._canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self._scrollbar = ttk.Scrollbar(self, orient="vertical",
                                        command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(self._canvas, bg=BG)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self.body, anchor="nw"
        )

        self.body.bind("<Configure>", self._on_body_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # numero domanda + testo
        self.q_num_label = tk.Label(self.body, text="", font=FONT_SMALL,
                                    bg=BG, fg=TEXT_DIM)
        self.q_num_label.pack(anchor="w", padx=40, pady=(24, 0))

        self.q_text = tk.Label(self.body, text="", font=FONT_H2,
                               bg=BG, fg=WHITE, wraplength=680,
                               justify="left")
        self.q_text.pack(anchor="w", padx=40, pady=(4, 20))

        # frame risposte
        self.ans_frame = tk.Frame(self.body, bg=BG)
        self.ans_frame.pack(fill="x", padx=40)

        # area feedback (sotto le risposte, nello scroll)
        self.feedback_frame = tk.Frame(self.body, bg=BG)
        self.feedback_frame.pack(fill="x", padx=40, pady=(16, 24))

    def _on_body_configure(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── mostra domanda ──────────────────────────────────────────────────────
    def _show_question(self):
        # pulisci
        for w in self.ans_frame.winfo_children():
            w.destroy()
        for w in self.feedback_frame.winfo_children():
            w.destroy()
        self.next_btn.pack_forget()
        self.result_badge.config(text="")
        # torna in cima
        self._canvas.yview_moveto(0)

        q = self.questions[self.idx]

        # header
        mode_txt = "📖 MODALITÀ STUDIO" if self.mode == "studio" else "🏆 QUIZ"
        self.mode_badge.config(text=mode_txt)
        self.prog_label.config(text=f"Domanda {self.idx+1} / {len(self.questions)}")
        self.pb_var.set(self.idx)

        self.q_num_label.config(text=f"# {q['num']}")
        self.q_text.config(text=q["domanda"])

        # shuffle risposte
        opts = [
            ("efficace",     q["efficace"]),
            ("media",        q["media"]),
            ("non_efficace", q["non_efficace"]),
        ]
        random.shuffle(opts)

        self._btn_refs = {}
        for key, text in opts:
            btn = self._make_answer_btn(key, text)
            btn.pack(fill="x", pady=5)
            self._btn_refs[key] = btn

        # in modalità studio mostra subito la risposta
        if self.mode == "studio":
            self._show_feedback(None)  # nessuna scelta utente

    def _make_answer_btn(self, key, text):
        frame = tk.Frame(self.ans_frame, bg=CARD_BG, cursor="hand2")
        frame.pack(fill="x", pady=0)  # packed from caller

        icon_map  = {"efficace": "●", "media": "●", "non_efficace": "●"}
        color_map = {"efficace": TEXT, "media": TEXT, "non_efficace": TEXT}

        icon  = tk.Label(frame, text=icon_map[key], font=FONT_SMALL,
                         bg=CARD_BG, fg=color_map[key], padx=8)
        icon.pack(side="left", pady=12)

        lbl = tk.Label(frame, text=text, font=FONT_BODY,
                       bg=CARD_BG, fg=TEXT, wraplength=620,
                       justify="left", padx=8, pady=12)
        lbl.pack(side="left", fill="x", expand=True)

        def click(_key=key, _frame=frame):
            self._on_answer(_key)

        for w in (frame, icon, lbl):
            w.bind("<Button-1>", lambda e, k=key: self._on_answer(k))
            w.bind("<Enter>",    lambda e, f=frame: f.config(bg="#3a3a55"))
            w.bind("<Leave>",    lambda e, f=frame: f.config(bg=CARD_BG) if not getattr(f, "_selected", False) else None)

        frame._label = lbl
        frame._icon  = icon
        return frame

    # ── gestione risposta ───────────────────────────────────────────────────
    def _on_answer(self, chosen_key):
        if self.mode == "quiz":
            # disabilita tutti i bottoni
            for k, f in self._btn_refs.items():
                for w in f.winfo_children():
                    w.unbind("<Button-1>")
                f.unbind("<Button-1>")
                f.unbind("<Enter>")
                f.unbind("<Leave>")
            self._show_feedback(chosen_key)
        # in studio non arriva qui (bottoni disabilitati)

    def _show_feedback(self, chosen_key):
        """Colora i bottoni, mostra feedback inline e aggiorna badge in basso."""
        q = self.questions[self.idx]

        color_key = {"efficace": GREEN,    "media": YELLOW,     "non_efficace": RED}
        dark_key  = {"efficace": GREEN_DK, "media": YELLOW_DK,  "non_efficace": RED_DK}
        mid_key   = {"efficace": GREEN_MID,"media": YELLOW_MID, "non_efficace": RED_MID}
        label_key = {
            "efficace":    "✅ Efficace",
            "media":       "⚡ Mediamente efficace",
            "non_efficace":"❌ Non efficace",
        }
        pts_key = {"efficace": "+1 pt", "media": "+0.5 pt", "non_efficace": "+0 pt"}

        # colora i pulsanti risposta
        for k, frame in self._btn_refs.items():
            if k == chosen_key:
                bg, fg = mid_key[k], WHITE
            else:
                bg, fg = dark_key[k], color_key[k]
            frame.config(bg=bg)
            for child in frame.winfo_children():
                child.config(bg=bg, fg=fg)

        # disabilita tutti i click/hover
        for k, frame in self._btn_refs.items():
            for w in [frame] + list(frame.winfo_children()):
                w.unbind("<Button-1>")
                w.unbind("<Enter>")
                w.unbind("<Leave>")

        # aggiorna punteggio
        if chosen_key:
            pts = self.SCORE_MAP[chosen_key]
            self.score += pts
            self.answers.append((q, chosen_key))
            self.score_label.config(text=f"{self.score:.1f}")
            badge_col  = color_key[chosen_key]
            badge_text = f"{label_key[chosen_key]}  {pts_key[chosen_key]}"
        else:
            self.answers.append((q, None))
            badge_col  = ACCENT
            badge_text = "📖 Modalità Studio"

        # ── badge nella barra fissa in basso ────────────────────────────────
        self.result_badge.config(text=badge_text, fg=badge_col)
        if self.idx + 1 < len(self.questions):
            self.next_btn.config(text="Prossima  →")
        else:
            self.next_btn.config(text="Vedi Risultati  🏆")
        self.next_btn.pack(side="right", padx=20)

        # ── legenda compatta inline (nello scroll, dopo le risposte) ─────────
        rows = [
            (GREEN,  GREEN_DK,  "✅ Efficace",           q["efficace"]),
            (YELLOW, YELLOW_DK, "⚡ Mediamente efficace", q["media"]),
            (RED,    RED_DK,    "❌ Non efficace",         q["non_efficace"]),
        ]
        for rc, rbg, rl, rt in rows:
            is_chosen = (
                (rc == GREEN  and chosen_key == "efficace") or
                (rc == YELLOW and chosen_key == "media")    or
                (rc == RED    and chosen_key == "non_efficace")
            )
            row_bg = mid_key[
                "efficace" if rc == GREEN else
                "media"    if rc == YELLOW else
                "non_efficace"
            ] if is_chosen else rbg

            row = tk.Frame(self.feedback_frame, bg=row_bg, padx=12, pady=8)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=rl, font=("Segoe UI", 10, "bold"),
                     bg=row_bg, fg=rc, width=22, anchor="w").pack(side="left")
            tk.Label(row, text=rt, font=FONT_SMALL, bg=row_bg,
                     fg=WHITE if is_chosen else TEXT,
                     wraplength=560, justify="left").pack(side="left", fill="x", expand=True)

        # scrolla giù per mostrare il feedback
        self.body.update_idletasks()
        self._canvas.yview_moveto(1.0)

    def _next(self):
        self.idx += 1
        if self.idx < len(self.questions):
            self._show_question()
        else:
            self.app.show_results(self.questions, self.answers, self.score, self.mode)


# ── schermata RISULTATI ───────────────────────────────────────────────────────

class ResultsScreen(tk.Frame):
    def __init__(self, master, app, questions, answers, score, mode):
        super().__init__(master, bg=BG)
        self.app       = app
        self.questions = questions
        self.answers   = answers
        self.score     = score
        self.mode      = mode
        self._build()

    def _build(self):
        total     = len(self.questions)
        max_score = float(total)
        pct       = (self.score / max_score * 100) if max_score else 0

        # titolo
        tk.Label(self, text="Risultati Finali", font=FONT_TITLE,
                 bg=BG, fg=WHITE).pack(pady=(40, 4))

        # score circle (simulato)
        color = GREEN if pct >= 70 else (YELLOW if pct >= 40 else RED)
        circle = tk.Label(self, text=f"{pct:.0f}%", font=("Segoe UI", 36, "bold"),
                          bg=BG, fg=color)
        circle.pack(pady=(10, 0))

        tk.Label(self, text=f"Punteggio: {self.score:.1f} / {max_score:.0f}",
                 font=FONT_H2, bg=BG, fg=TEXT).pack(pady=(4, 20))

        # stats
        stats_frame = tk.Frame(self, bg=CARD_BG, padx=30, pady=20)
        stats_frame.pack(padx=80, fill="x")

        efficaci   = sum(1 for _, k in self.answers if k == "efficace")
        medie      = sum(1 for _, k in self.answers if k == "media")
        non_eff    = sum(1 for _, k in self.answers if k == "non_efficace")
        no_ans     = sum(1 for _, k in self.answers if k is None)

        stats = [
            ("✅ Risposte Efficaci",           efficaci,  GREEN),
            ("⚡ Risposte Mediamente Efficaci", medie,     YELLOW),
            ("❌ Risposte Non Efficaci",         non_eff,   RED),
        ]
        if no_ans:
            stats.append(("📖 Osservate (studio)", no_ans, ACCENT))

        for label, val, col in stats:
            row = tk.Frame(stats_frame, bg=CARD_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=FONT_BODY, bg=CARD_BG, fg=TEXT,
                     width=34, anchor="w").pack(side="left")
            tk.Label(row, text=str(val), font=FONT_H2, bg=CARD_BG, fg=col).pack(side="right")

        # bottoni
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=30)

        HoverButton(btn_row, text="🔍 Rivedi le risposte", command=self._review,
                    bg="#3a3a55").pack(side="left", padx=8)
        HoverButton(btn_row, text="🔄 Nuovo quiz", command=self.app.restart,
                    bg=ACCENT).pack(side="left", padx=8)

    def _review(self):
        self.app.show_review(self.questions, self.answers)


# ── schermata REVISIONE ───────────────────────────────────────────────────────

class ReviewScreen(tk.Frame):
    SCORE_MAP = {"efficace": 1.0, "media": 0.5, "non_efficace": 0.0}
    ICON_MAP  = {"efficace": "✅", "media": "⚡", "non_efficace": "❌", None: "📖"}
    COLOR_MAP = {"efficace": GREEN, "media": YELLOW, "non_efficace": RED, None: ACCENT}

    def __init__(self, master, app, questions, answers):
        super().__init__(master, bg=BG)
        self.app = app
        self._build(questions, answers)

    def _build(self, questions, answers):
        hdr = tk.Frame(self, bg=CARD_BG, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔍  Riepilogo Risposte", font=FONT_H2,
                 bg=CARD_BG, fg=WHITE).pack(side="left", padx=20)
        HoverButton(hdr, text="← Risultati", command=self.app.back_to_results,
                    bg="#3a3a55", pady=6).pack(side="right", padx=20)

        sf = ScrollableFrame(self, bg=BG)
        sf.pack(fill="both", expand=True)
        inner = sf.inner

        for i, ((q, chosen), _q) in enumerate(zip(answers, questions)):
            col   = self.COLOR_MAP.get(chosen, ACCENT)
            icon  = self.ICON_MAP.get(chosen, "📖")
            pts   = self.SCORE_MAP.get(chosen, 0.0)

            card = tk.Frame(inner, bg=CARD_BG, padx=20, pady=14)
            card.pack(fill="x", padx=30, pady=6)

            # riga header
            top = tk.Frame(card, bg=CARD_BG)
            top.pack(fill="x")
            tk.Label(top, text=f"#{q['num']}  {icon}  +{pts}pt",
                     font=FONT_SMALL, bg=CARD_BG, fg=col).pack(side="left")

            tk.Label(card, text=q["domanda"], font=FONT_H2,
                     bg=CARD_BG, fg=WHITE, wraplength=680,
                     justify="left").pack(anchor="w", pady=(6, 10))

            # 3 righe risposte
            rows = [
                ("efficace",    GREEN,  "✅ Efficace"),
                ("media",       YELLOW, "⚡ Media"),
                ("non_efficace",RED,    "❌ Non efficace"),
            ]
            for key, rc, rlabel in rows:
                rw = tk.Frame(card, bg=CARD_BG)
                rw.pack(fill="x", pady=1)

                chosen_mark = " ◀ tua scelta" if key == chosen else ""
                lbl_text = f"{rlabel}{chosen_mark}"
                lbl_col  = WHITE if key == chosen else TEXT_DIM

                tk.Label(rw, text=lbl_text, font=FONT_SMALL, bg=CARD_BG,
                         fg=rc if key == chosen else TEXT_DIM,
                         width=28, anchor="w").pack(side="left")
                tk.Label(rw, text=q[key], font=FONT_SMALL, bg=CARD_BG,
                         fg=lbl_col, wraplength=480,
                         justify="left").pack(side="left")


# ── applicazione principale ───────────────────────────────────────────────────

class QuizApp:
    def __init__(self, root: tk.Tk):
        self.root       = root
        self.excel_path = None
        self._results_cache = None   # per tornare dai risultati
        root.title("Quiz Simulator")
        root.geometry("820x680")
        root.minsize(700, 560)
        root.configure(bg=BG)

        # frame contenitore
        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True)

        self._current = None
        self.show_welcome()

    def _switch(self, frame):
        if self._current:
            self._current.destroy()
        self._current = frame
        frame.pack(fill="both", expand=True)

    def show_welcome(self):
        self._switch(WelcomeScreen(self.container, self))

    def start_quiz(self, questions, mode):
        self._switch(QuizScreen(self.container, self, questions, mode))

    def show_results(self, questions, answers, score, mode):
        self._results_cache = (questions, answers, score, mode)
        self._switch(ResultsScreen(self.container, self, questions, answers, score, mode))

    def show_review(self, questions, answers):
        self._switch(ReviewScreen(self.container, self, questions, answers))

    def back_to_results(self):
        if self._results_cache:
            q, a, s, m = self._results_cache
            self._switch(ResultsScreen(self.container, self, q, a, s, m))

    def restart(self):
        self.show_welcome()


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
