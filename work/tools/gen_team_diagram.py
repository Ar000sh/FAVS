"""Generate work/ShareWise_Domain_Model.drawio: the team class diagram (17.10.26) as clean draw.io UML.

Every class is ONE draw.io cell with an HTML label (stereotype, name, attributes, methods), so draw.io
never re-lays out rows. Edit the model below and run:  python3 work/tools/gen_team_diagram.py
"""
import html, os

OUT = os.path.join(os.path.dirname(__file__), "..", "ShareWise_Domain_Model.drawio")

# ----------------------------------------------------------------------------------------------- model
# kind: root | entity | vo | enum | readmodel | events
C = {
    # Group context (supporting)
    "Group": ("root", ["+ id: GroupId", "+ name: GroupName", "+ currency: Currency", "+ status: GroupStatus"],
              ["+ createGroup(): GroupCreated",
               "+ inviteMember(Email, UserId adminOrMember): MemberInvited",
               "+ promoteToAdmin(UserId targetMember, UserId actingAdmin): MemberPromoted",
               "+ removeMember(UserId targetMember, UserId actingAdmin): MemberRemoved",
               "+ leaveGroup(UserId member): MemberLeft",
               "+ closeForSettlement(UserId actingAdmin): GroupClosedForSettlement",
               "+ reopenGroup(UserId actingAdmin): GroupReopened",
               "+ archiveGroup(UserId actingAdmin): GroupArchived",
               "+ acceptInvitation(InvitationId, UserId): MemberJoined",
               "+ declineInvitation(InvitationId): InvitationDeclined"]),
    "Membership": ("entity", ["+ userId: UserId", "+ role: GroupRole", "+ status: MembershipStatus",
                              "+ hasZeroBalance: boolean", "+ joinedAt: Instant"], []),
    "Invitation": ("entity", ["+ id: InvitationId", "+ email: Email", "+ status: InvitationStatus", "+ expiresAt: Instant"],
                   ["+ accept(UserId user)", "+ decline()"]),
    "GroupStatus": ("enum", ["OPEN", "CLOSED_FOR_SETTLEMENT", "ARCHIVED"], []),
    "GroupRole": ("enum", ["ADMIN", "MEMBER"], []),
    "MembershipStatus": ("enum", ["ACTIVE", "FORMER_MEMBER"], []),
    "InvitationStatus": ("enum", ["PENDING", "ACCEPTED", "DECLINED", "EXPIRED"], []),
    "GroupDomainEvents": ("events", ["GroupCreated", "MemberInvited", "MemberJoined", "MemberLeft", "MemberRemoved",
                                     "MemberPromoted", "InvitationDeclined", "GroupClosedForSettlement", "GroupReopened",
                                     "GroupArchived"], []),
    # Expense context (core)
    "Expense": ("root", ["+ id: ExpenseId", "+ groupId: GroupId", "+ paidBy: UserId", "+ recordedBy: UserId",
                         "+ title: ExpenseTitle", "+ totalAmount: Money", "+ splitStrategy: SplitStrategy",
                         "+ status: ExpenseStatus"],
                ["+ record(GroupMembershipView view, GroupId groupId, ExpenseTitle title,",
                 "      UserId paidBy, UserId recordedBy, Money totalAmount,",
                 "      List<ExpenseShare> shares, SplitStrategy splitStrategy): ExpenseRecorded",
                 "+ correct(GroupMembershipView view, Money newAmount, List<ExpenseShare> newShares,",
                 "      String reason, UserId actor): ExpenseCorrected",
                 "+ remove(GroupMembershipView view, UserId actor): ExpenseRemoved"]),
    "ExpenseShare": ("vo", ["+ participantId: UserId", "+ owedShare: Money"], []),
    "ExpenseRevision": ("vo", ["+ previousAmount: Money", "+ previousShares: List<ExpenseShare>", "+ correctedAt: Instant",
                               "+ correctedBy: UserId", "+ reason: String"], []),
    "SplitStrategy": ("enum", ["EQUAL", "EXACT", "PERCENTAGE"], []),
    "ExpenseStatus": ("enum", ["ACTIVE", "CORRECTED", "REMOVED"], []),
    "ExpenseDomainEvents": ("events", ["ExpenseRecorded", "ExpenseCorrected", "ExpenseRemoved"], []),
    "GroupMembershipView": ("readmodel", ["+ groupId: GroupId", "+ isOpen: boolean", "+ activeMembers: Set<UserId>",
                                          "+ admins: Set<UserId>"],
                            ["+ isActiveMember(UserId): boolean", "+ isAdmin(UserId): boolean"]),
    # Settlement context (core)
    "GroupLedger": ("root", ["+ groupId: GroupId"],
                    ["+ appendExpenseEntry(ExpenseRecorded)", "+ appendCorrectionReversal(ExpenseCorrected)",
                     "+ appendRemovalReversal(ExpenseRemoved)", "+ appendSettlementPayment(SettlementPaymentConfirmed)",
                     "+ appendDebtWaiver(DebtWaived)", "+ projectBalances(): List<MemberBalance>",
                     "+ projectSimplifiedPlan(): SettlementPlan"]),
    "LedgerEntry": ("entity", ["+ id: EntryId", "+ userId: UserId", "+ deltaAmount: Money", "+ type: LedgerEntryType",
                               "+ referenceId: String", "+ occurredAt: Instant"], []),
    "LedgerEntryType": ("enum", ["EXPENSE_PAID", "EXPENSE_OWED", "EXPENSE_REVERSAL", "PAYMENT_SENT",
                                 "PAYMENT_RECEIVED", "DEBT_WAIVED"], []),
    "MemberBalance": ("readmodel", ["+ userId: UserId", "+ netBalance: Money"], []),
    "SettlementPlan": ("readmodel", ["+ simplifiedDebts: List<DirectedDebt>"], []),
    "DirectedDebt": ("vo", ["+ fromDebtor: UserId", "+ toCreditor: UserId", "+ amount: Money"], []),
    "SettlementPayment": ("root", ["+ id: SettlementPaymentId", "+ groupId: GroupId", "+ fromDebtor: UserId",
                                   "+ toCreditor: UserId", "+ amount: Money", "+ status: PaymentStatus"],
                          ["+ record(Money openDebt): SettlementPaymentRecorded",
                           "+ confirm(UserId creditor): SettlementPaymentConfirmed",
                           "+ reject(UserId creditor, String note): SettlementPaymentRejected",
                           "+ waive(UserId creditor, String note): DebtWaived"]),
    "PaymentStatus": ("enum", ["PENDING", "CONFIRMED", "REJECTED", "WAIVED"], []),
    "SettlementDomainEvents": ("events", ["SettlementPaymentRecorded", "SettlementPaymentConfirmed",
                                          "SettlementPaymentRejected", "DebtWaived",
                                          "MemberBalanceStatusChanged", "AllBalancesSettled"], []),
    # Shared kernel
    "Money": ("vo", ["+ amount: BigDecimal", "+ currency: Currency"],
              ["+ add(Money): Money", "+ subtract(Money): Money", "+ negate(): Money", "+ isPositive(): boolean",
               "+ isZero(): boolean"]),
    "GroupId": ("vo", ["+ value: UUID"], []),
    # simple value objects instead of primitive types (DDD slide 66; GroupName listed on slide 68)
    "GroupName": ("vo", ["+ value: String"], []),
    "Email": ("vo", ["+ value: String"], []),
    "InvitationId": ("vo", ["+ value: UUID"], []),
    "ExpenseId": ("vo", ["+ value: UUID"], []),
    "ExpenseTitle": ("vo", ["+ value: String"], []),
    "EntryId": ("vo", ["+ value: UUID"], []),
    "SettlementPaymentId": ("vo", ["+ value: UUID"], []),
    "Currency": ("vo", ["+ code: String"], []),
    "UserId": ("vo", ["+ value: UUID"], []),
}

# ----------------------------------------------------------------------------------------------- drawing
STY = {  # fill, stroke, extra
    "root": ("#DAF5F9", "#0E8FA3", "strokeWidth=2;"), "entity": ("#DCE8FB", "#2A63C6", ""),
    "vo": ("#E3F4E1", "#3C8A3A", ""), "enum": ("#FFF6CC", "#B8960B", ""),
    "readmodel": ("#FCEAF4", "#B0458A", "dashed=1;"), "events": ("#EEE8FB", "#6A4FB3", ""),
}
STEREO = {"root": "Aggregate Root", "entity": "Entity", "vo": "Value Object", "enum": "Enumeration",
          "readmodel": "Read Model", "events": "Domain Events"}
CTX = {"core": ("#F3F6FC", "#2A63C6"), "sup": ("#FAF6EC", "#86681A"), "kernel": ("#F5F5F5", "#777777")}
AGG = ("#FFFFFF", "#0E8FA3")
CHAR, LINE, HEAD, PAD = 7.0, 15, 40, 10

cells, box = [], {}  # box[id] = (absx, absy, w, h)


def size(name):
    kind, attrs, methods = C[name]
    w = int(max([len(l) for l in attrs + methods] + [len(name) + 6, 18]) * CHAR + 28)
    h = HEAD + (len(attrs) * LINE + PAD if attrs else 0) + (len(methods) * LINE + PAD if methods else 0)
    return w, h


def container(cid, parent, x, y, w, h, title, fill, stroke, dashed=False):
    style = (f"rounded=1;arcSize={2 if dashed else 1};container=1;collapsible=0;html=1;whiteSpace=wrap;"
             f"verticalAlign=top;align=left;spacingLeft=12;spacingTop=6;fontStyle=1;fontSize={13 if dashed else 15};"
             f"fillColor={fill};strokeColor={stroke};fontColor={stroke};" + ("dashed=1;dashPattern=8 4;strokeWidth=2;" if dashed else ""))
    px, py = (box[parent][0], box[parent][1]) if parent != "1" else (0, 0)
    cells.append(f'<mxCell id="{cid}" value="{html.escape(title, quote=True)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    box[cid] = (px + x, py + y, w, h)


def note(cid, parent, x, y, w, h, text):
    style = ("shape=note;whiteSpace=wrap;html=1;size=14;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
             "spacingRight=8;fontSize=11;fillColor=#FFFDF2;strokeColor=#B8A77A;")
    cells.append(f'<mxCell id="{cid}" value="{html.escape(text, quote=True)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    box[cid] = (box[parent][0] + x, box[parent][1] + y, w, h)


def cls(name, parent, x, y):
    kind, attrs, methods = C[name]
    fill, stroke, extra = STY[kind]
    w, h = size(name)
    lab = (f'<p style="margin:0px;margin-top:5px;text-align:center;"><i>«{STEREO[kind]}»</i><br/>'
           f'<b>{html.escape(name)}</b></p>')
    for rows in (attrs, methods):
        if rows:
            lab += ('<hr size="1" style="border-style:solid;"/><p style="margin:0px;margin-left:8px;">'
                    + "<br/>".join(html.escape(r).replace("  ", "&nbsp;&nbsp;") for r in rows) + "</p>")
    style = (f"verticalAlign=top;align=left;overflow=fill;html=1;whiteSpace=wrap;fontSize=11;fontFamily=Helvetica;"
             f"fillColor={fill};strokeColor={stroke};{extra}")
    cells.append(f'<mxCell id="{name}" value="{html.escape(lab, quote=True)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    box[name] = (box[parent][0] + x, box[parent][1] + y, w, h)
    return w, h


n = [0]
BASE = "html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;fontSize=10;labelBackgroundColor=#FFFFFF;jumpStyle=arc;jumpSize=8;"
COMP = BASE + "endArrow=diamondThin;endFill=1;endSize=14;strokeColor=#333333;"
DASH = BASE + "dashed=1;endArrow=open;endFill=0;endSize=10;strokeColor=#666666;fontColor=#444444;"
PUB = BASE + "dashed=1;endArrow=open;endFill=0;endSize=10;strokeColor=#6A4FB3;fontColor=#6A4FB3;"
SUB = BASE + "dashed=1;endArrow=open;endFill=0;endSize=10;strokeWidth=1.6;strokeColor=#C0410D;fontColor=#C0410D;"


def edge(src, tgt, style, label="", exit=None, entry=None, points=(), mult=(None, None), label_at=None):
    n[0] += 1
    i = f"e{n[0]}"
    if exit: style += f"exitX={exit[0]:.3f};exitY={exit[1]:.3f};exitDx=0;exitDy=0;"
    if entry: style += f"entryX={entry[0]:.3f};entryY={entry[1]:.3f};entryDx=0;entryDy=0;"
    v = "" if label_at is not None else label
    pts = ("<Array as=\"points\">" + "".join(f'<mxPoint x="{x:.0f}" y="{y:.0f}"/>' for x, y in points) + "</Array>") if points else ""
    cells.append(f'<mxCell id="{i}" value="{html.escape(v, quote=True)}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">'
                 f'<mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
    if label_at is not None:
        cells.append(f'<mxCell id="{i}l" value="{html.escape(label)}" style="edgeLabel;html=1;fontSize=10;labelBackgroundColor=#FFFFFF;fontColor=#C0410D;" '
                     f'vertex="1" connectable="0" parent="{i}"><mxGeometry x="{label_at}" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')
    for pos, m in ((-1, mult[0]), (1, mult[1])):
        if m:
            cells.append(f'<mxCell id="{i}{"s" if pos < 0 else "t"}" value="{m}" style="edgeLabel;resizable=0;html=1;fontSize=10;labelBackgroundColor=none;'
                         f'align={"left" if pos < 0 else "right"};verticalAlign=bottom;" vertex="1" connectable="0" parent="{i}">'
                         f'<mxGeometry x="{0.8 * pos}" relative="1" as="geometry"><mxPoint x="{-6 if pos < 0 else 6}" y="-2" as="offset"/></mxGeometry></mxCell>')


def comp(part, whole, label="", mult=("1", "1")):
    """Composition drawn from the part's top up to the whole's bottom, entering above the part where possible."""
    px, py, pw, ph = box[part]; wx, wy, ww, wh = box[whole]
    fx = min(0.92, max(0.08, (px + pw / 2 - wx) / ww))
    edge(part, whole, COMP, label, exit=(0.5, 0), entry=(fx, 1), mult=mult)


def center_under(parent_name, w):
    x, _, pw, _ = box[parent_name]
    return x + (pw - w) / 2


GAP, ROWGAP = 50, 80

# ================================================================== Group context
G0 = (0, 0)
container("G", "1", G0[0], G0[1], 10, 10, "Group context · supporting · layered", *CTX["sup"])
container("AG", "G", 20, 50, 10, 10, "«Aggregate» Group · consistency boundary = 1 transaction", *AGG, dashed=True)
gw, gh = cls("Group", "AG", 20, 50)
r2 = 50 + gh + ROWGAP
mw, mh = size("Membership"); sw, sh = size("GroupStatus"); iw, ih = size("Invitation")
cls("Membership", "AG", 20, r2)
cls("GroupStatus", "AG", 20 + mw + GAP, r2)
cls("Invitation", "AG", 20 + mw + GAP + sw + GAP, r2)
r3 = r2 + max(mh, sh, ih) + ROWGAP
msw, msh = size("MembershipStatus")
cls("MembershipStatus", "AG", 20, r3)
cls("GroupRole", "AG", 20 + msw + 30, r3)
isw, _ = size("InvitationStatus")
cls("InvitationStatus", "AG", int(center_under("Invitation", isw) - box["AG"][0]), r3)
r4 = r3 + max(msh, size("InvitationStatus")[1]) + 60
x = 20
for nm in ("GroupName", "Email", "InvitationId"):
    w, _ = cls(nm, "AG", x, r4); x += w + 40
ag_w = max(20 + gw, 20 + mw + GAP + sw + GAP + iw, x - 40) + 20
ag_h = r4 + max(size(nm)[1] for nm in ("GroupName", "Email", "InvitationId")) + 30
cells[[i for i, c in enumerate(cells) if 'id="AG"' in c][0]] = cells[[i for i, c in enumerate(cells) if 'id="AG"' in c][0]].replace('width="10" height="10"', f'width="{ag_w}" height="{ag_h}"')
box["AG"] = (box["AG"][0], box["AG"][1], ag_w, ag_h)
gdw, gdh = cls("GroupDomainEvents", "G", 20 + ag_w + 60, 100)
# note on the 17.10 decision, below the events box
GNX, GNY, GNW, GNH = 20 + ag_w + 60, 100 + gdh + 50, 300, 175
note("noteInvite", "G", GNX, GNY, GNW, GNH,
     "<b>Decision 17.10: invitations go through the root</b><br/>"
     "What: Group.acceptInvitation() checks that the group is OPEN and the user is not yet a member, calls "
     "invitation.accept() (PENDING, not expired), adds the Membership and publishes MemberJoined. "
     "declineInvitation() works the same way. Invitation keeps accept() / decline(), but they only change its status.<br/>"
     "Why: aggregate rule 1 (DDD slide 67): rules that involve several parts are protected via the root. "
     "Events are published by the aggregate (slide 71), not by an inner entity.")
g_w = max(20 + ag_w + 60 + gdw, GNX + GNW) + 30
g_h = max(50 + ag_h, GNY + GNH) + 30
cells[0] = cells[0].replace('width="10" height="10"', f'width="{g_w}" height="{g_h}"')
box["G"] = (G0[0], G0[1], g_w, g_h)

comp("Membership", "Group", "manages", ("1..*", "1"))
comp("GroupStatus", "Group")
comp("Invitation", "Group", "tracks", ("0..*", "1"))
comp("MembershipStatus", "Membership")
comp("GroupRole", "Membership")
comp("InvitationStatus", "Invitation")
gx, gy, gw_, gh_ = box["Group"]; ex_, ey_, ew_, eh_ = box["GroupDomainEvents"]
edge("Group", "GroupDomainEvents", PUB, "publishes", exit=(1, (ey_ + 40 - gy) / gh_), entry=(0, 40 / eh_))

# ================================================================== Expense context
E0 = (g_w + 120, 0)
container("E", "1", E0[0], E0[1], 10, 10, "Expense context · core · hexagonal", *CTX["core"])
container("AE", "E", 20, 50, 10, 10, "«Aggregate» Expense · 1 transaction", *AGG, dashed=True)
xw, xh = cls("Expense", "AE", 20, 50)
r2 = 50 + xh + ROWGAP
x = 20
for nm in ("ExpenseShare", "ExpenseRevision", "SplitStrategy", "ExpenseStatus"):
    w, _ = cls(nm, "AE", x, r2); x += w + 40
row2_w = x - 40
r3 = r2 + max(size(nm)[1] for nm in ("ExpenseShare", "ExpenseRevision", "SplitStrategy", "ExpenseStatus")) + 60
x = 20
for nm in ("ExpenseId", "ExpenseTitle"):
    w, _ = cls(nm, "AE", x, r3); x += w + 40
ae_w = max(20 + xw, row2_w, x - 40) + 20
ae_h = r3 + max(size(nm)[1] for nm in ("ExpenseId", "ExpenseTitle")) + 30
i = [k for k, c in enumerate(cells) if 'id="AE"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{ae_w}" height="{ae_h}"'); box["AE"] = (box["AE"][0], box["AE"][1], ae_w, ae_h)
RC = 20 + ae_w + 60                                  # right column of the Expense context
gmw, gmh = cls("GroupMembershipView", "E", RC, 100)
cls("ExpenseDomainEvents", "E", RC, 100 + gmh + 70)
edw, edh = size("ExpenseDomainEvents")
# note on the 17.10 decision, below the events box and right of the line that enters it from below
NX, NY, NW, NH = RC + edw // 2 + 30, 100 + gmh + 70 + edh + 40, 300, 140
note("noteView", "E", NX, NY, NW, NH,
     "<b>Decision 17.10: GroupMembershipView</b><br/>"
     "What: Expense keeps a local copy of the group (open?, members, admins), updated from GroupDomainEvents, "
     "and gets it passed into record / correct / remove.<br/>"
     "Why: Expense only knows the groupId but must enforce R2/R3 (payer and participants are members), "
     "R5 (no changes when closed) and R6 (recorder, payer or admin). Same pattern as Membership.hasZeroBalance "
     "(DDD slide 67, rule 4: eventual consistency).")
e_w = max(RC + max(gmw, edw), NX + NW) + 30
e_h = max(50 + ae_h, NY + NH) + 30
i = [k for k, c in enumerate(cells) if 'id="E"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{e_w}" height="{e_h}"'); box["E"] = (E0[0], E0[1], e_w, e_h)

comp("ExpenseShare", "Expense", "splits into", ("1..*", "1"))
comp("ExpenseRevision", "Expense", "maintains history", ("0..*", "1"))
comp("SplitStrategy", "Expense")
comp("ExpenseStatus", "Expense")
xx, xy, xw_, xh_ = box["Expense"]; ex_, ey_, ew_, eh_ = box["ExpenseDomainEvents"]
y_pub = (max(xy, ey_) + min(xy + xh_, ey_ + eh_)) / 2           # level where Expense and its events box overlap
edge("Expense", "ExpenseDomainEvents", PUB, "publishes", exit=(1, (y_pub - xy) / xh_), entry=(0, (y_pub - ey_) / eh_))
vx, vy, vw, vh = box["GroupMembershipView"]
edge("Expense", "GroupMembershipView", DASH, "checks against (passed in)", exit=(1, (vy + 40 - xy) / xh_), entry=(0, 40 / vh))
# the view is kept up to date by the Group events: over the top of both contexts, down into GroupDomainEvents
GDE = box["GroupDomainEvents"]
edge("GroupMembershipView", "GroupDomainEvents", SUB,
     "subscribes to (MemberJoined, MemberLeft, MemberRemoved, MemberPromoted, GroupClosedForSettlement, GroupReopened, GroupArchived)",
     exit=(0.5, 0), entry=(0.5, 0), points=[(vx + vw / 2, -18), (GDE[0] + GDE[2] / 2, -18)], label_at=0.0)

# ================================================================== Settlement context
S0 = (0, max(g_h, e_h) + 140)
container("S", "1", S0[0], S0[1], 10, 10, "Settlement context · core · hexagonal (ledger + read models, CQRS)", *CTX["core"])
container("AL", "S", 20, 50, 10, 10, "«Aggregate» GroupLedger · 1 transaction", *AGG, dashed=True)
lw, lh = cls("GroupLedger", "AL", 20, 50)
lew, leh = size("LedgerEntry")
cls("LedgerEntry", "AL", int(20 + (lw - lew) / 2), 50 + lh + ROWGAP)
ltw, lth = size("LedgerEntryType")
cls("LedgerEntryType", "AL", int(20 + (lw - ltw) / 2), 50 + lh + ROWGAP + leh + ROWGAP)
eiw, eih = size("EntryId")
y_ei = 50 + lh + ROWGAP + leh + ROWGAP + lth + 60
cls("EntryId", "AL", int(20 + (lw - eiw) / 2), y_ei)
al_w, al_h = lw + 40, y_ei + eih + 30
i = [k for k, c in enumerate(cells) if 'id="AL"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{al_w}" height="{al_h}"'); box["AL"] = (box["AL"][0], box["AL"][1], al_w, al_h)

MID = 20 + al_w + 380                      # middle column: the context's events box + read models (wide gaps leave room for arrow labels)
sde_w, sde_h = cls("SettlementDomainEvents", "S", MID, 100)
mb_y = 100 + sde_h + 80
mbw, mbh = cls("MemberBalance", "S", MID, mb_y)
spw, sph = cls("SettlementPlan", "S", MID, mb_y + mbh + 60)
ddw, ddh = size("DirectedDebt")
cls("DirectedDebt", "S", int(MID + (spw - ddw) / 2), mb_y + mbh + 60 + sph + ROWGAP)
mid_w = max(sde_w, mbw, spw, ddw)

AP_X = MID + mid_w + 360
container("AP", "S", AP_X, 50, 10, 10, "«Aggregate» SettlementPayment · 1 transaction", *AGG, dashed=True)
pw, ph = cls("SettlementPayment", "AP", 20, 50)
psw, psh = size("PaymentStatus")
cls("PaymentStatus", "AP", int(20 + (pw - psw) / 2), 50 + ph + ROWGAP)
spiw, spih = size("SettlementPaymentId")
y_spi = 50 + ph + ROWGAP + psh + 60
cls("SettlementPaymentId", "AP", int(20 + (pw - spiw) / 2), y_spi)
ap_w, ap_h = pw + 40, y_spi + spih + 30
i = [k for k, c in enumerate(cells) if 'id="AP"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{ap_w}" height="{ap_h}"'); box["AP"] = (box["AP"][0], box["AP"][1], ap_w, ap_h)
s_w = AP_X + ap_w + 30
s_h = max(50 + al_h, 50 + ap_h, mb_y + mbh + 60 + sph + ROWGAP + ddh) + 40
i = [k for k, c in enumerate(cells) if 'id="S"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{s_w}" height="{s_h}"'); box["S"] = (S0[0], S0[1], s_w, s_h)

comp("LedgerEntry", "GroupLedger", "append-only entries", ("0..*", "1"))
comp("LedgerEntryType", "LedgerEntry")
comp("DirectedDebt", "SettlementPlan", "", ("0..*", "1"))
comp("PaymentStatus", "SettlementPayment")
L = box["GroupLedger"]; SDE = box["SettlementDomainEvents"]; MB = box["MemberBalance"]; SP = box["SettlementPlan"]
P = box["SettlementPayment"]; Sx, Sy = S0
y1, y2 = SDE[1] + 45, SDE[1] + SDE[3] - 30   # two separate horizontal lanes between GroupLedger and the events box
edge("GroupLedger", "SettlementDomainEvents", PUB, "publishes (MemberBalanceStatusChanged, AllBalancesSettled)",
     exit=(1, (y1 - L[1]) / L[3]), entry=(0, (y1 - SDE[1]) / SDE[3]))
edge("GroupLedger", "SettlementDomainEvents", SUB, "subscribes to (Confirmed, DebtWaived)",
     exit=(1, (y2 - L[1]) / L[3]), entry=(0, (y2 - SDE[1]) / SDE[3]))
edge("GroupLedger", "MemberBalance", DASH, "projects", exit=(1, min(0.95, (MB[1] + 30 - L[1]) / L[3])), entry=(0, 30 / MB[3]))
x_down = L[0] + L[2] - 20
edge("GroupLedger", "SettlementPlan", DASH, "computes", exit=((x_down - L[0]) / L[2], 1), entry=(0, 0.5),
     points=[(x_down, SP[1] + SP[3] / 2)])
y3 = SDE[1] + 45
edge("SettlementPayment", "SettlementDomainEvents", PUB, "publishes (Recorded, Confirmed, Rejected, DebtWaived)",
     exit=(0, (y3 - P[1]) / P[3]), entry=(1, (y3 - SDE[1]) / SDE[3]))

# ================================================================== Shared kernel (right of Settlement)
K0 = (s_w + 120, S0[1])
container("K", "1", K0[0], K0[1], 10, 10, "Shared kernel", *CTX["kernel"])
mw_, mh_ = cls("Money", "K", 30, 60)
cls("GroupId", "K", 30 + mw_ + 40, 60)
gidw, gidh = size("GroupId")
cls("UserId", "K", 30 + mw_ + 40, 60 + gidh + 40)
cw_, ch_ = size("Currency")
cls("Currency", "K", int(30 + (mw_ - cw_) / 2), 60 + mh_ + ROWGAP)
k_w = 30 + mw_ + 40 + max(gidw, size("UserId")[0]) + 30
k_h = 60 + max(mh_ + ROWGAP + ch_, gidh + 40 + size("UserId")[1]) + 30
i = [k for k, c in enumerate(cells) if 'id="K"' in c][0]
cells[i] = cells[i].replace('width="10" height="10"', f'width="{k_w}" height="{k_h}"'); box["K"] = (K0[0], K0[1], k_w, k_h)

comp("Currency", "Money")

# ================================================================== cross-context edges
M = box["Money"]; GI = box["GroupId"]; UI = box["UserId"]; X = box["Expense"]; EDE = box["ExpenseDomainEvents"]
# SettlementPayment *-- Money (amount): straight right into Money
yP = M[1] + 30
edge("Money", "SettlementPayment", COMP, "amount", exit=(0, (yP - M[1]) / M[3]), entry=(1, (yP - P[1]) / P[3]), mult=("1", "1"))
# Expense *-- Money (totalAmount) and Expense ..> GroupId / UserId: down a lane right of the Expense context
lane = box["E"][0] + box["E"][2] + 40
# the three lines leave Expense through the free gap between GroupMembershipView and ExpenseDomainEvents
V = box["GroupMembershipView"]; g_lo, g_hi = V[1] + V[3] + 12, EDE[1] - 12
fys = [(g_lo + (g_hi - g_lo) * k / 2 - X[1]) / X[3] for k in range(3)]
for k, (tgt, lbl, sty, fy) in enumerate((("Money", "totalAmount", COMP, fys[0]), ("GroupId", "references by ID", DASH, fys[1]),
                                       ("UserId", "references by ID", DASH, fys[2]))):
    T = box[tgt]; lx = lane + 18 * k; ty = T[1] - 30 - 12 * k if tgt != "UserId" else T[1] + T[3] / 2
    if tgt == "Money":
        edge(tgt, "Expense", COMP, lbl, exit=(0.7, 0), entry=(1, fy), points=[(T[0] + 0.7 * T[2], ty), (lx, ty), (lx, X[1] + fy * X[3])], mult=("1", "1"))
    elif tgt == "GroupId":
        edge("Expense", tgt, sty, lbl, exit=(1, fy), entry=(0.5, 0), points=[(lx, X[1] + fy * X[3]), (lx, ty), (T[0] + T[2] / 2, ty)])
    else:
        edge("Expense", tgt, sty, lbl, exit=(1, fy), entry=(1, 0.5), points=[(lx, X[1] + fy * X[3]), (lx + 0, ty), (T[0] + T[2] + 30, ty)])
# GroupLedger subscribes to ExpenseDomainEvents: up from the ledger, along the gap between the rows, up into the events
gap_y = S0[1] - 50
edge("GroupLedger", "ExpenseDomainEvents", SUB, "subscribes to", exit=(0.85, 0), entry=(0.5, 1),
     points=[(L[0] + 0.85 * L[2], gap_y), (EDE[0] + EDE[2] / 2, gap_y)], label_at=0.6)
# Group subscribes to SettlementDomainEvents: out of Group's left side, down the left margin, into the events box from above
gap_y2 = S0[1] - 25
Gr = box["Group"]
edge("Group", "SettlementDomainEvents", SUB, "subscribes to (MemberBalanceStatusChanged, AllBalancesSettled)",
     exit=(0, 0.5), entry=(0.5, 0), points=[(-40, Gr[1] + Gr[3] / 2), (-40, gap_y2), (SDE[0] + SDE[2] / 2, gap_y2)], label_at=0.55)

# ================================================================== title + legend
leg = ("<b style='font-size:18px'>ShareWise – class diagram (team version 17.10.26)</b><br/>"
       "Dashed boxes = aggregates (one transaction each). Aggregates refer to each other by ID only and react to each "
       "other's domain events (DDD slides 64–71). Purple dashed arrow = publishes, orange dashed arrow = subscribes to, "
       "◆ = composition (part of the aggregate), grey dashed = uses / references by ID. Colours: cyan aggregate root, "
       "blue entity, green value object, yellow enumeration, pink read model, purple domain events.")
cells.insert(0, f'<mxCell id="title" value="{html.escape(leg, quote=True)}" style="text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fontSize=12;fillColor=none;strokeColor=none;" vertex="1" parent="1">'
                f'<mxGeometry x="0" y="-130" width="1500" height="100" as="geometry"/></mxCell>')

xml = ('<mxfile host="app.diagrams.net"><diagram id="sharewise-team" name="ShareWise team model">'
       '<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
       'page="0" pageScale="1" pageWidth="3000" pageHeight="2400" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
with open(OUT, "w", encoding="utf-8") as f:
    f.write(xml)
print("written", OUT, len(cells), "cells")
